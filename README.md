# SQLBolt Lessons — explained with practical examples

My study notes for the free interactive course **[SQLBolt](https://sqlbolt.com/)**.
For each lesson: a plain-words explanation, the syntax, real examples, common mistakes and practice exercises with answers.

All examples run on one small practice database: a **car repair workshop** (customers, cars, mechanics, jobs). Every result shown in the lessons is the **real output** of the query, generated automatically.

## How to study

1. Do the lesson on [sqlbolt.com](https://sqlbolt.com/) (interactive exercises).
2. Read the matching lesson here for the "why" and more examples.
3. Practice on the workshop data with `tools/run.py` (below) before opening the answers.

## Lessons

| # | Lesson | You'll learn |
|---|---|---|
| 1 | [SELECT queries 101](lessons/01-select-queries.md) | read columns from a table |
| 2 | [Constraints pt. 1 — numbers](lessons/02-constraints-pt1.md) | `WHERE`, `=`, `>`, `BETWEEN`, `IN`, `AND`/`OR` |
| 3 | [Constraints pt. 2 — text](lessons/03-constraints-pt2.md) | `LIKE`, `%`, `_`, quotes |
| 4 | [Filtering and sorting](lessons/04-filtering-sorting.md) | `DISTINCT`, `ORDER BY`, `LIMIT`, `OFFSET` |
| 5 | [Review: simple SELECT](lessons/05-review-simple-select.md) | everything so far, on real questions |
| 6 | [JOINs](lessons/06-joins.md) | primary/foreign keys, `INNER JOIN` |
| 7 | [OUTER JOINs](lessons/07-outer-joins.md) | `LEFT`/`RIGHT`/`FULL JOIN`, finding missing matches |
| 8 | [NULLs](lessons/08-nulls.md) | `IS NULL`, `COALESCE`, NULL traps |
| 9 | [Expressions](lessons/09-expressions.md) | math, text, functions, aliases |
| 10 | [Aggregates pt. 1](lessons/10-aggregates-pt1.md) | `COUNT`, `SUM`, `AVG`, `GROUP BY` |
| 11 | [Aggregates pt. 2](lessons/11-aggregates-pt2.md) | `HAVING` vs `WHERE` |
| 12 | [Order of execution](lessons/12-order-of-execution.md) | how the database really runs a query |
| 13 | [Inserting rows](lessons/13-inserting-rows.md) | `INSERT`, constraint errors |
| 14 | [Updating rows](lessons/14-updating-rows.md) | `UPDATE … SET … WHERE` safely |
| 15 | [Deleting rows](lessons/15-deleting-rows.md) | `DELETE`, foreign keys, soft delete |
| 16 | [Creating tables](lessons/16-creating-tables.md) | `CREATE TABLE`, types, constraints |
| 17 | [Altering tables](lessons/17-altering-tables.md) | `ALTER TABLE`, migrations |
| 18 | [Dropping tables](lessons/18-dropping-tables.md) | `DROP TABLE` vs `DELETE` |
| X | [To infinity and beyond](lessons/19-to-infinity-and-beyond.md) | subqueries, `CASE`, `WITH`, `UNION`, window functions, indexes |

## The practice database

```
customers 1───* cars 1───* jobs *───1 mechanics
```

| Table | Columns |
|---|---|
| `customers` | id, name, city, phone *(can be NULL)*, joined_on |
| `cars` | id, customer_id → customers, make, model, year, plate |
| `mechanics` | id, name, specialty, hourly_rate, hired_on |
| `jobs` | id, car_id → cars, mechanic_id → mechanics *(can be NULL)*, service, labor_hours, parts_cost, opened_on, status |

Defined in [data/workshop.sql](data/workshop.sql). All data is made up.

## Try queries yourself

Only needs Python 3.11+ (no installs; its built-in SQLite must be 3.39+ for `RIGHT`/`FULL JOIN`). Every run starts from a fresh copy, so you can't break anything.

```bash
python tools/run.py
```

That opens an interactive prompt (`.tables`, `.schema`, `.reset`, `.quit`). Or run one query:

```bash
python tools/run.py "SELECT name, city FROM customers WHERE city = 'Caracas';"
```

## Editing the lessons

Inside `lessons/*.md`, every ```` ```sql ```` block is executed and its result is written below it:

- ```` ```sql ```` → runs, result inserted
- ```` ```sql error ```` → must fail; the error message is shown
- ```` ```sql norun ```` → never runs (syntax templates)

```bash
python tools/build.py
```

Check that every query works and every result is up to date (the test):

```bash
python tools/build.py --check
```
