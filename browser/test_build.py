"""Build contracts that protect the existing deployment and Google integration."""

import hashlib
import html
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from browser import build


class StaticBuildTests(unittest.TestCase):
    def test_extracts_complete_game_and_unchanged_integration(self):
        data = build.declarations()
        output = build.render()
        self.assertEqual(output.count('class="card" draggable="true"'), 27)
        self.assertEqual(output.count('class="bucket" data-type='), 31)
        self.assertIn(data['GOOGLE_FORM_ACTION'], output)
        self.assertIn(data['LEADERBOARD_CSV_URL'], output)
        for field_id in data['FORM_FIELD_IDS'].values():
            self.assertIn(field_id, output)
        for card in data['card_data']:
            self.assertIn(html.escape(card['text']), output)
        self.assertIn("mode: 'no-cors'", output)
        self.assertIn('const WARMUP_SECONDS = 20;', output)
        self.assertIn('const SHOT_CLOCK_SECONDS = 15;', output)
        self.assertIn('Google does not confirm receipt here', output)
        self.assertNotRegex(output, r'__[A-Z_]+__')

    def test_has_only_local_asset_references(self):
        output = build.render()
        urls = re.findall(r'(?:src|href)="([^"]+)"', output)
        self.assertTrue(urls)
        self.assertTrue(all(not url.startswith(('http', '/', 'data:')) for url in urls), urls)
        self.assertNotIn('stlite', output)
        self.assertNotIn('pyodide', output)

    def test_deterministic_hash_verified_output(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / 'first'
            second = Path(directory) / 'second'
            manifest = build.build(first)
            self.assertEqual(manifest, build.build(second))
            for filename, entry in manifest['files'].items():
                self.assertEqual(hashlib.sha256((first / filename).read_bytes()).hexdigest(), entry['sha256'])
            lock = json.loads((build.ROOT / 'browser/vendor-lock.json').read_text())
            for filename, entry in lock['files'].items():
                self.assertEqual(manifest['files'][f'vendor/{filename}']['sha256'], entry['sha256'])
            self.assertTrue((first / '.nojekyll').is_file())

    def test_changed_server_or_template_marker_is_rejected(self):
        with patch.object(build, 'BASELINE_SHA256', 'invalid'):
            with self.assertRaisesRegex(ValueError, 'Server game changed'):
                build.declarations()
        with self.assertRaisesRegex(ValueError, 'compatibility marker'):
            build.replace_once('marker marker', 'marker', 'value')

    def test_checkout_root_output_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Build output'):
            build.build(build.ROOT)


if __name__ == '__main__':
    unittest.main()
