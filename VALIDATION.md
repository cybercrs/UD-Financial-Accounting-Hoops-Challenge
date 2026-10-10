# Hoops static validation — 2026-10-10

Repository: cybercrs/UD-Financial-Accounting-Hoops-Challenge. Baseline/main:
`e3098d25934011b14c36bf8445e9bb8e900cc205`. Isolated source branch:
`browser/static-hoops`; static publishing branch: `hoops-browser-preview`.

## Passed checks

- Five build contract tests: full game extraction, unchanged Google identifiers,
  local asset paths, deterministic hashes, drift rejection, safe output location.
- Eight actual Chromium scenarios. The final run is recorded in
  [browser-results.json](review/browser-results.json).
- Ruff 0.14.0 on the original server wrapper and all new browser Python;
  Python compilation with the prepared Hoops Python 3.14.7 runtime;
  Node 24 syntax checks on generated game JavaScript and the vendored polyfill;
  Git whitespace check. See review/unit.log and review/lint.log.
- Repeated builds produce identical file hashes. App output: 13 hashed files,
  4,440,431 bytes, plus manifest.json. Screenshots and validation notes are
  additional review artifacts rather than runtime dependencies.
- All pre-existing tracked files, including streamlit_app.py, requirements.txt,
  .python-version, artwork/audio, .devcontainer/, and existing .github/ files,
  are byte-identical to main. The new CI workflow is limited to source-branch
  pushes and only validates/builds; it has no deployment/write permissions.

## Browser evidence

The walkthrough uses real rendered controls and local assets at both `/` and
`/UD-Financial-Accounting-Hoops-Challenge/`, with all external requests blocked.
Only the exact published-CSV GET and exact Form POST are intercepted with test
responses. Zero requests are forwarded to Google and no public records are
created. The mock POST produces an actual opaque browser response; that is
explicitly not treated as confirmed receipt.

- An unmodified real-time 20-second warm-up rejected attempts to match. A
  keyboard correct answer earned 10, and viewing rankings during the real
  15-second shot clock still produced the -2 violation.
- A complete 27-card game included a wrong answer at zero, another after one
  correct match, and ended at 268. All six POST fields, identity normalization,
  unique attempt ID, score, and completion time were validated against source.
- Duplicate matched-card attempts, completion-board interactions, and repeated
  leaderboard review caused no new scoring or POST. The completion timer stopped.
- Intro form drafts and active selected-card drafts survived leaderboard review.
  Rankings retained the best snapshot after stale and failed CSV refreshes.
- A second full game tested a failed mock POST and the actual Play Again control.
  Play Again and refresh reset score, matches, identity, timer and attempt ID;
  card order reshuffled. Future view/stage/hash claims never unlocked completion.
- Tabs in one browser context and separate contexts remained independent.
- Enter/Space matching, Escape focus return, desktop drag/drop, 390px touch/tap
  matching, audio asset readiness, and absence of horizontal layout overflow
  passed. No unexpected external asset requests or JavaScript execution errors.

The complete-game scenarios use Playwright's virtual clock to avoid repeated
real-time waits. Their recorded completion times and screenshots are synthetic
test evidence, not performance results. The first timer scenario uses real time.

Screenshots: [intro](review/intro.png), [desktop board](review/desktop-board.png),
[completion with mock rankings](review/completed.png),
[390px intro](review/narrow-intro.png), [390px board](review/narrow-board.png).
Visual inspection confirmed legible controls and scrolling. The narrow intro
requires scrolling its modal to reach all fields, as the original does; the
game retains its compact card text. Real mobile hardware remains untested.

## Game navigation interpretation

This game exposes all questions together on one continuously timed board.
There are no earned lesson pages to revisit, so stage Back/Forward is
inapplicable. No navigation is added that could pause/reopen timed gameplay,
re-score earlier answers, or unlock future questions. Existing intro/ranking
overlays and post-completion locked-board viewing remain. The original generic
rankings view hides Play Again when reopened after closing completion; a page
refresh starts a new challenge. No unrelated game rules were changed.

Hoops originally has no persistent progress/bookmark payload. Refresh and
reopened bookmarks intentionally reset the game; URLs never carry student
identity or scores. During-document drafts and sessions retain their behavior.

## Not run and activation requirements

- Existing Hoops unit/AppTest suite: none supplied. New build tests and actual
  browser UI scenarios cover this static extraction; no server Streamlit is
  installed into a browser runtime.
- Live Google receipt test: not run; authorization for synthetic public records
  was not given. The canonical published-Sheets read-only GET was attempted and
  blocked by the cloud proxy: `Tunnel connection failed: 403 Forbidden`. See
  [google-read.json](review/google-read.json). No alternate route was attempted.
- Hosted HTTPS browser and public deployment verification: not run. Current
  tools cannot enable Pages. GitHub repository metadata reported `has_pages:
  false` before publishing; no existing site is replaced.
- Real-device/browser matrix, simultaneous classroom load, and Google service
  capacity/reliability: not measured. No claim for 40–45 or 80–135 learners.

Activation in the same repository: **Settings → Pages → Deploy from a branch
→ hoops-browser-preview → /(root) → Save**. Check that no site was activated
since the recorded inspection before saving. Wait for the Pages build to pass,
then verify the actual public URL and run a hosted browser check through an
allowed network. The known cybercrs.github.io proxy restriction must be respected.

Source and publishing commits, final remote-main verification, and GitHub CI
state are returned in the handoff after pushing; neither branch is merged.
