"""Shared helpers: load the practice database and run SQL text against it.

Used by run.py (try queries yourself) and build.py (fills the results into the lessons).
Only uses Python's standard library — no installs needed.
"""

import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "data" / "workshop.sql"
MAX_ROWS = 25


def fresh_db() -> sqlite3.Connection:
    """A brand-new in-memory copy of the workshop database."""
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SEED.read_text(encoding="utf-8"))
    return con


def split_statements(sql: str) -> list[str]:
    """Split text into complete SQL statements (safe with ';' inside strings)."""
    statements, buf = [], ""
    for ch in sql:
        buf += ch
        if ch == ";" and sqlite3.complete_statement(buf):
            statements.append(buf.strip())
            buf = ""
    if buf.strip() and not _only_comments(buf):
        statements.append(buf.strip())
    return statements


_COMMENTS = re.compile(r"/\*.*?(\*/|$)|--[^\n]*", re.S)
QUERY_VERBS = {"SELECT", "WITH", "VALUES", "PRAGMA", "EXPLAIN"}


def _strip_comments(text: str) -> str:
    return _COMMENTS.sub(" ", text).strip()


def _only_comments(text: str) -> bool:
    return not _strip_comments(text)


def _first_word(stmt: str) -> str:
    code = _strip_comments(stmt)
    return code.split(None, 1)[0].upper() if code else ""


class RunError(Exception):
    """A statement failed. `partial` holds the results of the statements before it."""

    def __init__(self, error: sqlite3.Error, partial: list[dict]):
        super().__init__(str(error))
        self.partial = partial


def run(con: sqlite3.Connection, sql: str) -> list[dict]:
    """Run every statement. Returns one entry per statement:
    {"columns": [...], "rows": [...]} for queries, {"changed": n, "verb": ...} for the rest.
    On failure raises RunError (with the results that did run)."""
    out = []
    for stmt in split_statements(sql):
        if _only_comments(stmt):
            continue
        before = con.total_changes
        verb = _first_word(stmt)
        try:
            cur = con.execute(stmt)
            rows = cur.fetchall() if cur.description else None
        except sqlite3.Error as e:
            raise RunError(e, out) from e
        if cur.description and (verb in QUERY_VERBS or " RETURNING " in f" {stmt.upper()} "):
            out.append({"columns": [d[0] for d in cur.description], "rows": rows})
        else:
            con.commit()
            out.append({"changed": con.total_changes - before, "verb": verb})
    return out


def fmt_value(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, float):
        s = f"{v:.12g}"  # real value; hides only float noise like 0.30000000000000004
        return s + ".0" if s.lstrip("-").isdigit() else s
    return str(v)


def to_markdown(results: list[dict]) -> str:
    """Render results as Markdown (tables for queries, a short note for changes)."""
    parts = []
    for r in results:
        if "columns" in r:
            cols, rows = r["columns"], r["rows"]
            if not rows:
                parts.append("*(no rows)*")
                continue
            esc = lambda s: s.replace("|", "\\|")
            lines = ["| " + " | ".join(esc(c) for c in cols) + " |",
                     "|" + "|".join("---" for _ in cols) + "|"]
            for row in rows[:MAX_ROWS]:
                lines.append("| " + " | ".join(esc(fmt_value(v)) for v in row) + " |")
            if len(rows) > MAX_ROWS:
                lines.append(f"\n*… {len(rows) - MAX_ROWS} more rows*")
            lines.append(f"\n*{len(rows)} row{'s' if len(rows) != 1 else ''}*")
            parts.append("\n".join(lines))
        else:
            verb, n = r["verb"], r["changed"]
            if verb in ("INSERT", "UPDATE", "DELETE", "REPLACE") or n > 0:
                parts.append(f"✔ {verb} OK — {n} row{'s' if n != 1 else ''} affected")
            else:
                parts.append(f"✔ {verb} OK")
    return "\n\n".join(parts)


def to_text(results: list[dict]) -> str:
    """Render results as an aligned plain-text table (for the terminal)."""
    parts = []
    for r in results:
        if "columns" not in r:
            parts.append(to_markdown([r]))
            continue
        cols = r["columns"]
        rows = [[fmt_value(v) for v in row] for row in r["rows"]]
        widths = [max([len(c)] + [len(row[i]) for row in rows]) for i, c in enumerate(cols)]
        line = lambda cells: "  ".join(c.ljust(w) for c, w in zip(cells, widths)).rstrip()
        text = [line(cols), "  ".join("-" * w for w in widths)] + [line(r_) for r_ in rows]
        text.append(f"({len(rows)} row{'s' if len(rows) != 1 else ''})")
        parts.append("\n".join(text))
    return "\n\n".join(parts)
