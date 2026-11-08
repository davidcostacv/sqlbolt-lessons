"""Runs every ```sql block in lessons/*.md and writes its REAL result right below it.

    python tools/build.py           # update the results in every lesson
    python tools/build.py --check   # fail if any query errors or a result is out of date (the test)

Rules for ```sql blocks:
  ```sql          → runs; result is inserted between <!-- result --> markers
  ```sql error    → must FAIL; the error message is shown (to teach what goes wrong)
  ```sql norun    → never runs (syntax templates with placeholders)
Each lesson gets its own fresh database, and blocks run top to bottom,
so an INSERT earlier in a lesson is visible to a SELECT later in the same lesson.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sqltool import ROOT, RunError, fresh_db, run, to_markdown  # noqa: E402

LESSONS = ROOT / "lessons"
BLOCK = re.compile(
    r"(?P<fence>^```sql(?P<flag>[ \t]+\w+)?[ \t]*\n(?P<sql>.*?)^```[ \t]*\n)"
    r"(?P<old>\n?<!-- result -->\n.*?<!-- /result -->\n)?",
    re.S | re.M,
)


class LessonError(Exception):
    pass


def read(path: Path) -> str:
    # Normalize Windows line endings so the block regex always matches.
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return text if text.endswith("\n") else text + "\n"


def render(path: Path) -> str:
    text = read(path)
    fences = len(re.findall(r"^```sql", text, re.M))
    found = len(BLOCK.findall(text))
    if fences != found:
        raise LessonError(f"{path.name}: {fences} ```sql fences but only {found} parsed — check formatting")
    con = fresh_db()

    def replace(m):
        flag = (m["flag"] or "").strip()
        sql = m["sql"]
        if flag == "norun":
            return m["fence"]
        line = text.count("\n", 0, m.start()) + 1
        try:
            body = to_markdown(run(con, sql))
            if flag == "error":
                raise LessonError(f"{path.name}:{line}: block marked 'error' but it succeeded")
        except RunError as e:
            if flag != "error":
                raise LessonError(f"{path.name}:{line}: {e}\n{sql}") from e
            body = f"❌ Error: `{e}`"
            if e.partial:
                body = to_markdown(e.partial) + "\n\n" + body
        return f"{m['fence']}\n<!-- result -->\n**Result:**\n\n{body}\n<!-- /result -->\n"

    return BLOCK.sub(replace, text)


def main():
    check = "--check" in sys.argv
    files = sorted(LESSONS.glob("*.md"))
    if not files:
        print("No lessons found.")
        return 1
    stale, errors, blocks = [], [], 0
    for f in files:
        try:
            new = render(f)
        except LessonError as e:
            errors.append(str(e))
            continue
        blocks += len(BLOCK.findall(new))
        if new != read(f):
            if check:
                stale.append(f.name)
            else:
                f.write_text(new, encoding="utf-8", newline="\n")
    for e in errors:
        print("ERROR", e)
    for s in stale:
        print("OUT OF DATE", s, "→ run: python tools/build.py")
    ok = not errors and not stale
    print(f"{'OK' if ok else 'FAILED'}: {len(files)} lessons, {blocks} sql blocks")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
