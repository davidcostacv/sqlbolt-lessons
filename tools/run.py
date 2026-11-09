"""Try SQL yourself against the workshop practice database.

    python tools/run.py "SELECT * FROM cars;"     # run one query
    python tools/run.py my_query.sql              # run a file
    python tools/run.py                           # interactive mode (type .quit to exit)

Every run starts from a fresh copy of the data, so experiment freely —
DELETE everything if you want, nothing is saved.
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sqltool import RunError, fresh_db, run, to_text  # noqa: E402

TABLES_HELP = "Tables: customers, cars, mechanics, jobs   (.tables / .schema / .reset / .quit)"


def execute(con, sql):
    try:
        print(to_text(run(con, sql)))
    except RunError as e:
        if e.partial:
            print(to_text(e.partial) + "\n")
        print(f"Error: {e}")


def repl():
    con = fresh_db()
    print("Workshop practice DB (in memory). End queries with ;")
    print(TABLES_HELP)
    buf = ""
    while True:
        try:
            line = input("sql> " if not buf else "...> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        line = line.replace("﻿", "")  # PowerShell pipes can add an invisible BOM
        cmd = line.strip()
        if not buf and cmd in (".quit", ".exit", "exit", "quit"):
            return
        if not buf and cmd == ".tables":
            execute(con, "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            continue
        if not buf and cmd == ".schema":
            for (s,) in con.execute("SELECT sql FROM sqlite_master WHERE type='table'"):
                print(s + ";\n")
            continue
        if not buf and cmd == ".reset":
            con = fresh_db()
            print("Data reset to the original copy.")
            continue
        buf += line + "\n"
        if sqlite3.complete_statement(buf):
            execute(con, buf)
            buf = ""


def main():
    if len(sys.argv) < 2:
        repl()
        return
    arg = sys.argv[1]
    path = Path(arg)
    if path.suffix.lower() == ".sql" and " " not in arg.strip():
        if not path.exists():
            print(f"Error: file not found: {arg}")
            sys.exit(1)
        sql = path.read_text(encoding="utf-8-sig")  # -sig drops a BOM (Notepad/PowerShell add one)
    else:
        sql = arg
    execute(fresh_db(), sql)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
