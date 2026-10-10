# Browser asset notices

The original repository LICENSE and assets/AUDIO_SOURCES.md apply to the game
and its artwork/audio and are included in the static output.

The existing mobile drag/drop dependency is locally packaged from the exact
`mobile-drag-drop@2.3.0-rc.2` jsDelivr URLs used by the server. vendor-lock.json
records the bytes and SHA-256 checksums; builds verify them and require no
network. The JS header labels its built version 2.3.0-rc.1; these are the actual
bytes served by the original 2.3.0-rc.2 package URL, not a version upgrade.

Upstream: https://github.com/timruffles/mobile-drag-drop

## MIT License — mobile-drag-drop

Copyright (c) 2019 Tim Ruffles

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
