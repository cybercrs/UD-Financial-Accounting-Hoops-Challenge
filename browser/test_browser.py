"""Actual local Chromium game walkthroughs. Every Google request is mocked."""

from __future__ import annotations

import functools
import http.server
import json
import os
import tempfile
import threading
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs

from playwright.sync_api import expect, sync_playwright

from browser.build import ROOT, build, declarations

REVIEW = ROOT / "browser/review"
CSV = (
    'First Name,Last Initial,Section,High Score,Best Time (seconds),Data As Of\n'
    'Demo,A,MOCK,270,12.5,2026-10-10 12:00:00\n'
    'Other,B,MOCK,260,15.2,2026-10-10 12:00:00\n'
    'Test,S,999,999,1,2026-10-10 12:00:00\n'
)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def snapshot(page):
    return page.evaluate("""() => ({score, matchedCount, currentAttemptId,
        gameStartedAt, completionTimeSeconds, attemptComplete, warmupActive,
        selected: selectedItem?.id, shotClockDeadline,
        matches: Array.from(document.querySelectorAll('.bucket .card')).map(c => c.id),
        order: cards.map(c => c.id)})""")


def start(page, *, virtual=True):
    page.locator('#first-name').fill('Demo')
    page.locator('#last-initial').fill('a')
    page.locator('#section-number').fill('MOCK')
    page.get_by_role('button', name='Begin Warm-Up').click()
    expect(page.locator('#player-modal')).not_to_have_class('modal-backdrop is-open')
    assert snapshot(page)['warmupActive']
    if virtual:
        page.clock.run_for(20_100)
    else:
        expect(page.locator('#shot-clock-label')).to_have_text('SHOT CLOCK', timeout=25_000)
    assert not snapshot(page)['warmupActive']


def match(page, card, *, keyboard=False):
    target = card.get_attribute('data-target')
    # Attribute equality avoids substrings such as Supplies / Supplies Expense.
    bucket = page.locator(f'.bucket[data-type={json.dumps(target)}]')
    if keyboard:
        card.focus()
        page.keyboard.press('Enter')
        bucket.focus()
        page.keyboard.press('Space')
    else:
        card.click()
        bucket.click()


def run():
    REVIEW.mkdir(parents=True, exist_ok=True)
    results = []
    external = []
    posts = []
    errors = []
    mock_state = {'fail_post': False, 'csv': CSV, 'fail_csv': False}
    integration = declarations()
    with tempfile.TemporaryDirectory(prefix='hoops-browser-') as directory:
        webroot = Path(directory)
        subdir = 'UD-Financial-Accounting-Hoops-Challenge'
        build(webroot)
        build(webroot / subdir)
        server = http.server.ThreadingHTTPServer(
            ('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(webroot)))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}'
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=os.environ.get('CHROMIUM_EXECUTABLE', '/usr/bin/chromium'), headless=True)

            def intercept(route):
                request = route.request
                if request.url.startswith(base + '/'):
                    route.continue_()
                elif request.url == integration['GOOGLE_FORM_ACTION'] and request.method == 'POST':
                    posts.append(parse_qs(request.post_data or ''))
                    if mock_state['fail_post']:
                        route.abort('failed')
                    else:
                        route.fulfill(status=200, body='mock only', content_type='text/plain')
                elif request.url.startswith(integration['LEADERBOARD_CSV_URL']) and request.method == 'GET':
                    if mock_state['fail_csv']:
                        route.abort('failed')
                    else:
                        route.fulfill(status=200, body=mock_state['csv'],
                                      headers={'access-control-allow-origin': '*', 'content-type': 'text/csv'})
                else:
                    external.append({'url': request.url, 'method': request.method})
                    route.abort('blockedbyclient')

            contexts = []

            def new_page(path='/', *, virtual=True, width=1280, height=900, touch=False):
                context = browser.new_context(viewport={'width': width, 'height': height}, has_touch=touch)
                contexts.append(context)
                context.route('**/*', intercept)
                page = context.new_page()
                page.set_default_timeout(10_000)
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.add_init_script("""window.mockFetchTypes = [];
                    const originalFetch = window.fetch;
                    window.fetch = (...args) => originalFetch(...args).then(response => {
                        window.mockFetchTypes.push({url: String(args[0]), type: response.type});
                        return response;
                    });""")
                if virtual:
                    instant = datetime(2026, 10, 10, 12, tzinfo=timezone.utc)
                    page.clock.install(time=instant)
                    page.clock.pause_at(instant + timedelta(seconds=1))
                response = page.goto(base + path, wait_until='load')
                assert response.status == 200
                expect(page.locator('#player-modal-title')).to_have_text('Welcome to the Challenge')
                return page

            def check(name, callback):
                before = len(posts)
                print(f'Running: {name}', flush=True)
                try:
                    callback()
                    result = {'check': name, 'status': 'passed', 'mock_form_posts': len(posts) - before}
                except Exception:
                    result = {'check': name, 'status': 'failed', 'error': traceback.format_exc()}
                results.append(result)
                print(json.dumps(result), flush=True)

            def real_timer_flow():
                page = new_page(virtual=False)
                assert page.locator('#card-pool .card').count() == 27
                assert page.locator('.bucket').count() == 31
                page.get_by_role('button', name='Begin Warm-Up').click()
                expect(page.locator('#player-form-error')).to_contain_text('valid first name')
                assert snapshot(page)['gameStartedAt'] is None
                page.locator('#first-name').fill('Demo')
                page.locator('#last-initial').fill('a')
                page.locator('#section-number').fill('MOCK')
                page.get_by_role('button', name='Begin Warm-Up').click()
                card = page.locator('#card-pool .card').first
                match(page, card)
                assert snapshot(page)['score'] == 0 and snapshot(page)['matchedCount'] == 0
                expect(page.locator('#shot-clock-label')).to_have_text('SHOT CLOCK', timeout=25_000)
                match(page, card, keyboard=True)
                expect(page.locator('#score')).to_have_text('10')
                assert page.evaluate('getComputedStyle(document.activeElement).outlineStyle') != 'none'
                page.get_by_role('button', name='Leaderboard', exact=True).click()
                expect(page.locator('#leaderboard-body tr')).to_have_count(2)
                # Rankings must not pause the clock or reopen a warm-up.
                expect(page.locator('#score')).to_have_text('8', timeout=18_000)
                page.keyboard.press('Escape')
                assert snapshot(page)['matchedCount'] == 1
                assert page.evaluate('document.activeElement.id') == 'leaderboard-button'
                assert page.locator('#success-sound').evaluate('(a) => a.readyState') >= 2
                assert page.locator('#buzzer-sound').evaluate('(a) => a.readyState') >= 2
                page.screenshot(path=str(REVIEW / 'desktop-board.png'))
                page.context.close()

            check('real 20s warm-up; keyboard match; audio loaded; leaderboard clock violation', real_timer_flow)

            def complete_flow():
                page = new_page('/' + subdir + '/')
                page.screenshot(path=str(REVIEW / 'intro.png'))
                page.locator('#first-name').fill('Demo')
                page.get_by_role('button', name='View Leaderboard').click()
                expect(page.locator('#leaderboard-body tr')).to_have_count(2)
                page.get_by_role('button', name='Close leaderboard').click()
                expect(page.locator('#first-name')).to_have_value('Demo')
                start(page)
                first = page.locator('#card-pool .card').first
                wrong = page.locator('.bucket').filter(has_not=page.locator('.bucket-label', has_text=first.get_attribute('data-target'))).first
                first.click()
                wrong.click()
                expect(page.locator('#score')).to_have_text('0')
                assert snapshot(page)['matchedCount'] == 0
                match(page, first)
                expect(page.locator('#score')).to_have_text('10')
                # Repeating a previously matched card earns nothing.
                before = snapshot(page)
                page.evaluate("attemptMatch(cards.find(c => c.getAttribute('draggable') === 'false'), buckets[0])")
                assert snapshot(page) == before
                next_card = page.locator('#card-pool .card').first
                next_card.click()
                wrong = page.locator(f'.bucket:not([data-type={json.dumps(next_card.get_attribute("data-target"))}])').first
                wrong.click()
                expect(page.locator('#score')).to_have_text('8')
                assert page.locator('#miss-sound').evaluate('(a) => a.readyState') >= 2
                # Keep a selected draft through ranking review without a timer tick.
                draft = snapshot(page)
                page.get_by_role('button', name='Leaderboard', exact=True).click()
                expect(page.locator('#leaderboard-body tr')).to_have_count(2)
                page.keyboard.press('Escape')
                assert snapshot(page) == draft
                while page.locator('#card-pool .card').count():
                    match(page, page.locator('#card-pool .card').first, keyboard=True)
                page.clock.run_for(700)
                expect(page.locator('#leaderboard-modal-title')).to_have_text('Challenge Complete!')
                expect(page.locator('#save-status')).to_contain_text('Google does not confirm receipt here')
                assert snapshot(page)['score'] == 268
                assert snapshot(page)['matchedCount'] == 27
                fields = integration['FORM_FIELD_IDS']
                sent = posts[-1]
                assert set(sent) == set(fields.values())
                assert sent[fields['first_name']] == ['Demo']
                assert sent[fields['last_initial']] == ['A']
                assert sent[fields['section_number']] == ['MOCK']
                assert sent[fields['score']] == ['268']
                assert sent[fields['attempt_id']] == [snapshot(page)['currentAttemptId']]
                assert float(sent[fields['completion_time']][0]) >= 0.01
                assert page.evaluate("mockFetchTypes.some(r => r.url === GOOGLE_FORM_ACTION && r.type === 'opaque')")
                page.screenshot(path=str(REVIEW / 'completed.png'))
                completed = snapshot(page)
                posted = len(posts)
                page.get_by_role('button', name='Close leaderboard').click()
                page.locator('.bucket').first.click()
                page.clock.run_for(31_000)
                assert snapshot(page) == completed
                page.get_by_role('button', name='Leaderboard', exact=True).click()
                page.keyboard.press('Escape')
                assert snapshot(page) == completed and len(posts) == posted
                # The original header opens generic rankings, even after completion.
                # Reset from the completion overlay is tested before leaving it below.
                page.reload(wait_until='load')
                expect(page.locator('#player-modal')).to_have_class('modal-backdrop is-open')
                fresh = snapshot(page)
                assert fresh['score'] == 0 and fresh['matchedCount'] == 0
                assert fresh['currentAttemptId'] != completed['currentAttemptId']
                assert fresh['order'] != completed['order']
                page.context.close()

            check('subdirectory complete game; wrong answers; repeats; drafts; locked completion; opaque mock POST; reset', complete_flow)

            def refresh_flow():
                page = new_page('/?view=999&stage=complete&score=270#results')
                assert not snapshot(page)['attemptComplete'] and snapshot(page)['gameStartedAt'] is None
                assert not page.locator('#completion-score').is_visible()
                start(page)
                match(page, page.locator('#card-pool .card').first)
                before = snapshot(page)
                page.reload(wait_until='load')
                after = snapshot(page)
                assert after['score'] == 0 and after['matchedCount'] == 0
                assert after['currentAttemptId'] != before['currentAttemptId']
                assert after['order'] != before['order']
                assert page.evaluate('localStorage.length + sessionStorage.length') == 0
                expect(page.locator('#first-name')).to_have_value('')
                assert not page.locator('#completion-score').is_visible()
                page.context.close()

            check('future query/hash rejected; refresh/bookmark starts new game; no stored identity', refresh_flow)

            def isolation_flow():
                first = new_page()
                second = first.context.new_page()
                second.on('pageerror', lambda error: errors.append(str(error)))
                second.goto(base + '/', wait_until='load')
                third = new_page()
                assert len({snapshot(page)['currentAttemptId'] for page in [first, second, third]}) == 3
                start(first)
                match(first, first.locator('#card-pool .card').first)
                for page in [second, third]:
                    assert snapshot(page)['score'] == 0 and snapshot(page)['gameStartedAt'] is None
                    expect(page.locator('#first-name')).to_have_value('')
                first.context.close()
                third.context.close()

            check('same-context tabs and independent browser sessions', isolation_flow)

            def narrow_flow():
                page = new_page(width=390, height=844, touch=True)
                page.screenshot(path=str(REVIEW / 'narrow-intro.png'))
                start(page)
                card = page.locator('#card-pool .card').first
                target = card.get_attribute('data-target')
                card.tap()
                page.locator(f'.bucket[data-type={json.dumps(target)}]').tap()
                expect(page.locator('#score')).to_have_text('10')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                assert page.evaluate('document.getElementById("main-container").scrollWidth <= innerWidth')
                assert page.get_by_role('button', name='Leaderboard', exact=True).bounding_box()['height'] >= 38
                page.screenshot(path=str(REVIEW / 'narrow-board.png'))
                page.context.close()

            check('390px touch/tap gameplay, layout, and narrow screenshots', narrow_flow)

            def drag_flow():
                page = new_page()
                start(page)
                card = page.locator('#card-pool .card[data-target="Cash Account"]')
                bucket = page.locator('.bucket[data-type="Cash Account"]')
                card.drag_to(bucket)
                expect(page.locator('#score')).to_have_text('10')
                assert snapshot(page)['matchedCount'] == 1
                page.context.close()

            check('native desktop drag/drop', drag_flow)

            def integration_failure_flow():
                page = new_page()
                mock_state['fail_post'] = True
                start(page)
                while page.locator('#card-pool .card').count():
                    match(page, page.locator('#card-pool .card').first)
                page.clock.run_for(700)
                expect(page.locator('#save-status')).to_contain_text('could not be sent')
                expect(page.locator('#leaderboard-body tr')).to_have_count(2)
                mock_state['csv'] = 'First Name,Last Initial,Section,High Score,Best Time (seconds),Data As Of\nDemo,A,MOCK,10,99,2026-10-09 12:00:00\n'
                page.get_by_role('button', name='Refresh', exact=True).click()
                expect(page.locator('#leaderboard-status')).to_contain_text('Showing 2 of 2')
                assert page.locator('#leaderboard-body tr').first.locator('td').nth(3).inner_text() == '270'
                mock_state['fail_csv'] = True
                page.get_by_role('button', name='Refresh', exact=True).click()
                expect(page.locator('#leaderboard-status')).to_contain_text('latest refresh failed')
                expect(page.locator('#leaderboard-body tr')).to_have_count(2)
                previous = snapshot(page)['currentAttemptId']
                page.get_by_role('button', name='Play Again').click()
                expect(page.locator('#player-modal')).to_have_class('modal-backdrop is-open')
                assert snapshot(page)['currentAttemptId'] != previous
                assert snapshot(page)['score'] == 0
                page.context.close()
                mock_state.update(fail_post=False, fail_csv=False, csv=CSV)

            check('failed POST; stale and failed CSV retain best prior snapshot', integration_failure_flow)
            browser.close()
        server.shutdown()
        server.server_close()
    results.append({'check': 'no unexpected external requests or JavaScript errors',
                    'status': 'passed' if not external and not errors else 'failed',
                    'unexpected_requests': external, 'javascript_errors': errors})
    report = {'browser': 'Chromium', 'google': 'mocked; zero live submissions',
              'real_google_submission': 'not run', 'hosted_https_browser': 'not run',
              'classroom_capacity': 'not measured', 'results': results}
    (REVIEW / 'browser-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'passed': sum(r['status'] == 'passed' for r in results), 'total': len(results)}))
    return 1 if any(r['status'] != 'passed' for r in results) else 0


if __name__ == '__main__':
    raise SystemExit(run())
