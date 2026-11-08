# Lesson 16 — Creating tables

📘 SQLBolt: https://sqlbolt.com/lesson/creating_tables · [← Prev](15-deleting-rows.md) · [Next →](17-altering-tables.md)

## The idea in plain words

`CREATE TABLE` defines a new table: its name, its columns, the **type** of each column, and the **rules** (constraints) the data must follow.

Designing the table well is the cheapest way to keep data clean — the database itself refuses data that breaks the rules, so your app doesn't have to check everything.

> SQLite note: the **constraints** below are enforced, but the **types** are only a suggestion (`'abc'` fits in an `INTEGER` column). Add `STRICT` after the closing parenthesis — `CREATE TABLE t (…) STRICT;` — to make SQLite check types like PostgreSQL does.

## Syntax

```sql norun
CREATE TABLE IF NOT EXISTS table_name (
    column  TYPE  CONSTRAINTS  DEFAULT value,
    column2 TYPE  CONSTRAINTS,
    …
);
```

`IF NOT EXISTS` → don't error if the table is already there.

### Common types

| Type | For | Example |
|---|---|---|
| `INTEGER` | whole numbers | `year`, `id`, `quantity` |
| `REAL` / `FLOAT` | decimals | `hourly_rate` |
| `TEXT` / `VARCHAR(n)` | text | `name`, `plate` |
| `BOOLEAN` | true/false (SQLite stores 1/0) | `is_paid` |
| `DATE` / `DATETIME` | dates (SQLite stores them as text `'YYYY-MM-DD'`) | `opened_on` |

> 💰 For real money, many databases have `DECIMAL(10,2)`/`NUMERIC` to avoid rounding errors, or you store **cents** as an `INTEGER` (1999 = $19.99).

### Common constraints

| Constraint | Means |
|---|---|
| `PRIMARY KEY` | the unique id of each row |
| `AUTOINCREMENT` | (with an integer primary key) never reuse old ids |
| `NOT NULL` | value is required |
| `UNIQUE` | no two rows can have the same value |
| `DEFAULT x` | value used when you don't give one |
| `CHECK (condition)` | custom rule, e.g. `CHECK (price >= 0)` |
| `REFERENCES other(id)` | **foreign key**: must point to an existing row |

## Practical example — an invoices table for the workshop

```sql
CREATE TABLE invoices (
    id         INTEGER PRIMARY KEY,
    job_id     INTEGER NOT NULL UNIQUE REFERENCES jobs(id),
    total_usd  REAL    NOT NULL CHECK (total_usd >= 0),
    is_paid    BOOLEAN NOT NULL DEFAULT 0,
    issued_on  TEXT    NOT NULL DEFAULT (DATE('now'))
);
```

<!-- result -->
**Result:**

✔ CREATE OK
<!-- /result -->

What each rule does for us:
- `job_id … UNIQUE` → one invoice per job, never two.
- `REFERENCES jobs(id)` → can't invoice a job that doesn't exist.
- `CHECK (total_usd >= 0)` → no negative invoices.
- `DEFAULT 0` → new invoices start as unpaid without us saying so.

Let's use it:

```sql
INSERT INTO invoices (job_id, total_usd) VALUES (1, 71.0);
```

<!-- result -->
**Result:**

✔ INSERT OK — 1 row affected
<!-- /result -->

```sql
SELECT id, job_id, total_usd, is_paid FROM invoices;
```

<!-- result -->
**Result:**

| id | job_id | total_usd | is_paid |
|---|---|---|---|
| 1 | 1 | 71.0 | 0 |

*1 row*
<!-- /result -->

The rules in action — a negative total:

```sql error
INSERT INTO invoices (job_id, total_usd) VALUES (2, -10);
```

<!-- result -->
**Result:**

❌ Error: `CHECK constraint failed: total_usd >= 0`
<!-- /result -->

A second invoice for job 1:

```sql error
INSERT INTO invoices (job_id, total_usd) VALUES (1, 50);
```

<!-- result -->
**Result:**

❌ Error: `UNIQUE constraint failed: invoices.job_id`
<!-- /result -->

## Bonus: a table from a query

You can create a table already filled with the result of a `SELECT` — handy for reports or backups:

```sql
CREATE TABLE done_jobs AS
SELECT id, service, parts_cost FROM jobs WHERE status = 'done';
```

<!-- result -->
**Result:**

✔ CREATE OK
<!-- /result -->

```sql
SELECT COUNT(*) AS rows_copied FROM done_jobs;
```

<!-- result -->
**Result:**

| rows_copied |
|---|
| 10 |

*1 row*
<!-- /result -->

(This copies the data but **not** the constraints.)

## Good habits

- Name tables in plural (`invoices`) and columns in `snake_case` (`issued_on`).
- Every table gets an `id INTEGER PRIMARY KEY`.
- Use `NOT NULL` by default; allow NULL only when "unknown" is meaningful.
- In SQLite, foreign keys are only enforced after `PRAGMA foreign_keys = ON;` (this repo turns it on for you).

## Practice

Create a `parts` table: id, part name (required), brand, price (required, ≥ 0), stock (whole number, default 0). Insert two parts and select them.

<details><summary>Answer</summary>

```sql
CREATE TABLE parts (
    id     INTEGER PRIMARY KEY,
    name   TEXT    NOT NULL,
    brand  TEXT,
    price  REAL    NOT NULL CHECK (price >= 0),
    stock  INTEGER NOT NULL DEFAULT 0
);
INSERT INTO parts (name, brand, price, stock) VALUES ('Injector', 'Bosch', 80.0, 6);
INSERT INTO parts (name, brand, price) VALUES ('Brake pad set', 'Brembo', 45.0);
SELECT * FROM parts;
```

<!-- result -->
**Result:**

✔ CREATE OK

✔ INSERT OK — 1 row affected

✔ INSERT OK — 1 row affected

| id | name | brand | price | stock |
|---|---|---|---|---|
| 1 | Injector | Bosch | 80.0 | 6 |
| 2 | Brake pad set | Brembo | 45.0 | 0 |

*2 rows*
<!-- /result -->

</details>
