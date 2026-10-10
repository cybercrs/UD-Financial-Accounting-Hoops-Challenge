"""Extract the existing game without importing or changing its server wrapper."""

from __future__ import annotations

import argparse
import ast
import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA256 = "7d5360935676d4942412b3c18e479ac7991a83a2a36e78a209a37c3b203a04de"
ASSETS = {
    "__HOOP_IMAGE_URI__": "UD Hoop.png",
    "__BASKETBALL_IMAGE_URI__": "UD Basketball.png",
    "__SUCCESS_SOUND_URI__": "assets/basketball-through-net.wav",
    "__MISS_SOUND_URI__": "assets/basketball-hard-hit.wav",
    "__BUZZER_SOUND_URI__": "assets/basketball-buzzer.wav",
}


def declarations() -> dict:
    source = (ROOT / "streamlit_app.py").read_bytes()
    if hashlib.sha256(source).hexdigest() != BASELINE_SHA256:
        raise ValueError("Server game changed: review static compatibility before building")
    names = {
        "GOOGLE_FORM_ACTION", "LEADERBOARD_CSV_URL", "FORM_FIELD_IDS",
        "card_data", "bucket_sections", "game_template",
    }
    values = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    values[target.id] = ast.literal_eval(node.value)
    if values.keys() != names:
        raise ValueError("Missing expected game declarations")
    return values


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"Expected one compatibility marker: {old[:80]}")
    return text.replace(old, new)


def render() -> str:
    data = declarations()
    cards = []
    for index, card in enumerate(data["card_data"]):
        text = card["text"]
        text_class = "card-text"
        if len(text) > 115:
            text_class += " card-text--compact"
        elif len(text) > 90:
            text_class += " card-text--dense"
        cards.append(
            f'<div class="card" draggable="true" data-target="{html.escape(card["target"], quote=True)}" '
            f'id="card-{index}" role="button" tabindex="0" aria-label="{html.escape(text, quote=True)}">'
            '<img class="card-art" alt="" aria-hidden="true">'
            f'<span class="{text_class}">{html.escape(text)}</span></div>'
        )
    sections = []
    for title, section_class, buckets in data["bucket_sections"]:
        sections.append(
            f'<section class="section {section_class}"><h2 class="section-header">'
            f'{html.escape(title)}</h2><div class="bucket-grid">'
            + "".join(
                f'<div class="bucket" data-type="{html.escape(bucket, quote=True)}" '
                f'aria-label="{html.escape(bucket, quote=True)} hoop" role="button" tabindex="0">'
                '<img class="bucket-art" alt="" aria-hidden="true">'
                f'<span class="bucket-label">{html.escape(bucket)}</span></div>'
                for bucket in buckets
            ) + '</div></section>'
        )
    replacements = {
        **{marker: quote(path, safe="/") for marker, path in ASSETS.items()},
        "__CARDS_HTML__": "".join(cards),
        "__SECTIONS_HTML__": "".join(sections),
        "__GOOGLE_FORM_ACTION__": data["GOOGLE_FORM_ACTION"],
        "__LEADERBOARD_CSV_URL__": data["LEADERBOARD_CSV_URL"],
        **{f"__FORM_{key.upper()}__": value for key, value in data["FORM_FIELD_IDS"].items()},
    }
    output = data["game_template"]
    for old, new in replacements.items():
        output = replace_once(output, old, new)
    if re.search(r"__[A-Z_]+__", output):
        raise ValueError("Unresolved game template placeholder")
    output = replace_once(output, '<head>', '<head>\n<title>UD Financial Accounting Hoops Challenge</title>')
    output = replace_once(output, 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no',
                          'width=device-width, initial-scale=1.0')
    for filename in ("default.css", "index.min.js"):
        output = replace_once(output,
                              f"https://cdn.jsdelivr.net/npm/mobile-drag-drop@2.3.0-rc.2/{filename}",
                              f"vendor/{filename}")
    # The wrapper shuffles on rerun. A static app instead shuffles on every load,
    # including Play Again, while retaining stable cards throughout each attempt.
    shuffle = """    const shuffledCards = Array.from(document.querySelectorAll('#card-pool .card'));
    for (let index = shuffledCards.length - 1; index > 0; index -= 1) {
        const other = Math.floor(Math.random() * (index + 1));
        [shuffledCards[index], shuffledCards[other]] = [shuffledCards[other], shuffledCards[index]];
    }
    document.getElementById('card-pool').append(...shuffledCards);

"""
    output = replace_once(output, "    const cards = Array.from(document.querySelectorAll('.card'));",
                          shuffle + "    const cards = Array.from(document.querySelectorAll('.card'));")
    output = replace_once(output, 'Your result is being added below. Rankings update automatically and may take a few minutes.',
                          'Your score submission is being attempted. Rankings may take a few minutes to update.')
    output = replace_once(output, 'Score sent. The leaderboard will continue checking for updated rankings.',
                          'Score submission attempted. Google does not confirm receipt here. Check the leaderboard after it updates.')
    # Clarify the preserved reset contract; no identity/score is saved in URLs.
    output = replace_once(output, '<h3 id="intro-guide-title">How to play</h3>',
                          '<h3 id="intro-guide-title">How to play</h3>\n'
                          '            <p class="privacy-note">Refreshing or reopening this page starts a new challenge.</p>')
    return output.lstrip()


def build(destination: Path) -> dict:
    destination = destination.resolve()
    if destination == ROOT or ROOT in destination.parents and destination.parts[len(ROOT.parts)] != "browser":
        raise ValueError("Build output must be outside the checkout or within browser/")
    destination.mkdir(parents=True, exist_ok=True)
    lock = json.loads((ROOT / "browser/vendor-lock.json").read_text())
    for filename, entry in lock["files"].items():
        source = ROOT / "browser/vendor" / filename
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry["sha256"]:
            raise ValueError(f"Vendor checksum mismatch: {filename}")
        target = destination / "vendor" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    for path in (*ASSETS.values(), "assets/AUDIO_SOURCES.md", "LICENSE"):
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, target)
    shutil.copyfile(ROOT / "browser/THIRD_PARTY_NOTICES.md", destination / "THIRD_PARTY_NOTICES.md")
    (destination / "index.html").write_text(render(), encoding="utf-8")
    (destination / ".nojekyll").write_text("")
    files = {
        path.relative_to(destination).as_posix(): {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size,
        }
        for path in sorted(destination.rglob("*")) if path.is_file() and path.name != "manifest.json"
    }
    manifest = {"server_baseline": "e3098d25934011b14c36bf8445e9bb8e900cc205", "files": files}
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "browser/dist")
    args = parser.parse_args()
    manifest = build(args.output)
    print(f"Built {len(manifest['files'])} files; {sum(f['bytes'] for f in manifest['files'].values()):,} bytes")


if __name__ == "__main__":
    main()
