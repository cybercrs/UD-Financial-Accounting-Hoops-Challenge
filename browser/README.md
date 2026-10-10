# Hoops browser version

This is a direct static HTML/JavaScript extraction of the existing game. It
does not need stlite, Pyodide, Streamlit, Python, a server session, or a new
repository to play. The build uses Python's standard library to read literal
declarations from the unchanged server wrapper without importing it. A pinned
server-source hash and checked replacement markers reject unreviewed changes.

From the repository root in the saved Accounting Teaching Apps environment:

```bash
/workspace/.cloud-setup/venvs/hoops/bin/python -m browser.build
/workspace/.cloud-setup/venvs/main/bin/python -m unittest browser.test_build -v
/workspace/.cloud-setup/venvs/main/bin/python -m browser.test_browser
```

For a manual local preview, serve browser/dist over HTTP with Python's
`http.server`; file URLs are unsupported. The browser harness creates its own
temporary HTTP server at both root and the repository-name subdirectory.
It blocks external traffic and mocks all Google requests; it never posts
synthetic scores to the public leaderboard. Review evidence is in review/.

## Game flow and navigation

Hoops has one continuous board with intro and leaderboard overlays. The
20-second warm-up, 15-second shot clock, 27 randomly ordered definition balls,
31 hoops, +10 correct answers, -2 incorrect answers and clock violations,
zero score floor, completion time, keyboard/tap/drag interactions, and audio
are retained. Cards reshuffle on each page load, as they did on server rerun.

There are no earned lesson pages to review. Stage Back/Forward arrows would
reopen timed/scored gameplay or create a pause. They are therefore inapplicable
here. The existing leaderboard open/close and Escape controls remain available;
viewing rankings leaves the ongoing game clock running. Completion leaves the
board locked and does not offer re-scoring. Play Again starts a fresh attempt.

The original game stores no progress, identity, drafts, score, or attempt ID in
local storage or bookmarks. Refresh and reopened bookmarks start a new game,
including when a query/hash claims a later stage. Form drafts survive opening
and closing the intro leaderboard in the current document. Tabs and browser
contexts are independent. This migration deliberately preserves that contract.

## Google integration

The exact Form endpoint, six field identifiers, and published Sheets CSV URL
come from the source wrapper. Submission still uses direct `no-cors` POST;
successful fetch completion is an opaque response and does not confirm receipt.
The UI now says so. Google access, sharing, security, formulas, and destinations
are unchanged. LEADERBOARD_SETUP.md documents the existing setup.

All artwork, audio and the same mobile-drag-drop assets are local. Vendored
assets were retrieved with certificate verification and are checked against
vendor-lock.json. See THIRD_PARTY_NOTICES.md for notices. Build output is about
4.4 MB; functional tests do not establish classroom capacity for 40–45 or
80–135 simultaneous users, Google write reliability, or real-device support.

## Separate GitHub Pages publishing

Source branch: `browser/static-hoops`. Static-only publishing branch:
`hoops-browser-preview`. Main and all server deployment files stay unchanged.
Before every activation/update, inspect remote branches and Pages settings.
Never replace an existing Pages site.

The static branch contains the generated root index.html, vendor/, assets/,
artwork, .nojekyll, hashes, notices, and validation evidence. For initial
activation when no site already exists: open repository **Settings → Pages**,
choose **Deploy from a branch**, choose **hoops-browser-preview**, folder
**/(root)**, and save. No current tool enables Pages. Wait for the Pages build
to succeed, then verify the actual public URL and repeat a hosted browser
check. No public URL is claimed before that verification.

Main must never be merged or used as the Pages publishing source for this
migration. To rebuild, review the server-source hash, run the build and tests,
and publish only the generated output to the separate static branch.
