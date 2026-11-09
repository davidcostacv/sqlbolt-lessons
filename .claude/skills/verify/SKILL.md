---
name: verify
description: How to verify changes in sqlbolt-lessons by running the real tools (run.py prompt, lessons rendered by GitHub).
---

# Verify sqlbolt-lessons

Surfaces: the `tools/run.py` CLI (one-shot + interactive prompt) and the lessons as GitHub renders them.

## Recipe
1. Fresh clone into the scratchpad: `gh repo clone davidcostacv/sqlbolt-lessons` (user has `core.autocrlf=true`; `.gitattributes` keeps LF — confirm with `file lessons/*.md`, no "CRLF").
2. One-shot: `python tools/run.py "SELECT name FROM customers;"` and a `.sql` file path.
3. Interactive: pipe a session **from PowerShell** (the user's shell), e.g. `.tables`, a multi-line query, `DELETE FROM jobs;` → `.reset` → count is 15 again.
4. Rendering: `gh api repos/davidcostacv/sqlbolt-lessons/contents/lessons/<file>.md -H "Accept: application/vnd.github.html"` → count `<table`, `<details`, and make sure no `&lt;!-- result` is visible.

## Gotchas
- PowerShell 5.1 here pipes UTF-8 **with a BOM** (`\xef\xbb\xbf`) and Out-File utf8 writes a BOM. run.py strips it; always probe a piped first line and a BOM `.sql` file.
- The built-in browser pane can't screenshot local `file://` HTML — use the gh renderer output instead.
- `python tools/build.py --check` is the repo's test (run it before committing, not as verification).
