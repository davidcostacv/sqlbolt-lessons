# Lesson 18 — Dropping tables

📘 SQLBolt: https://sqlbolt.com/lesson/dropping_tables · [← Prev](17-altering-tables.md) · [Next →](19-to-infinity-and-beyond.md)

## The idea in plain words

`DROP TABLE` deletes a **whole table**: the data **and** the structure. It's gone.

Compare:

| Command | Rows | The table itself |
|---|---|---|
| `DELETE FROM t;` | all deleted | still exists (empty) |
| `DROP TABLE t;` | all deleted | **gone** |

## Syntax

```sql norun
DROP TABLE IF EXISTS table_name;
```

`IF EXISTS` → no error if the table isn't there (useful in setup scripts that may run twice).

## Practical examples

We made a temporary report table:

```sql
CREATE TABLE report_2025 AS
SELECT status, COUNT(*) AS jobs FROM jobs GROUP BY status;
```

<!-- result -->
**Result:**

✔ CREATE OK
<!-- /result -->

```sql
SELECT * FROM report_2025;
```

<!-- result -->
**Result:**

| status | jobs |
|---|---|
| done | 10 |
| in progress | 3 |
| open | 2 |

*3 rows*
<!-- /result -->

We don't need it anymore:

```sql
DROP TABLE report_2025;
```

<!-- result -->
**Result:**

✔ DROP OK
<!-- /result -->

It's really gone — querying it now fails:

```sql error
SELECT * FROM report_2025;
```

<!-- result -->
**Result:**

❌ Error: `no such table: report_2025`
<!-- /result -->

Running it again with `IF EXISTS` doesn't complain:

```sql
DROP TABLE IF EXISTS report_2025;
```

<!-- result -->
**Result:**

✔ DROP OK
<!-- /result -->

## Foreign keys protect you here too

`cars` is referenced by `jobs`. Dropping `cars` while jobs still point at it is refused:

```sql error
DROP TABLE cars;
```

<!-- result -->
**Result:**

❌ Error: `FOREIGN KEY constraint failed`
<!-- /result -->

You'd have to drop the tables that depend on it first — `jobs` → `cars` → `customers`. Children first, like in Lesson 15. (PostgreSQL also offers `DROP TABLE cars CASCADE`, which removes the links for you — powerful and dangerous.)

```sql
DROP TABLE jobs;
DROP TABLE cars;
```

<!-- result -->
**Result:**

✔ DROP OK

✔ DROP OK
<!-- /result -->

```sql
SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name;
```

<!-- result -->
**Result:**

| name |
|---|
| customers |
| mechanics |

*2 rows*
<!-- /result -->

(`sqlite_master` is SQLite's own list of everything in the database.)

## Real-life safety rules

- **Backup first.** In real projects, never run `DROP TABLE` on production without a backup.
- Use `IF EXISTS` in scripts, never in a hurry by hand.
- Double-check which database you're connected to. Dropping a table in "test" is fine; in "production" it's a very bad day.

## Practice

1. Create a table `tmp_cities` with the distinct customer cities, check it, then drop it.

<details><summary>Answer</summary>

```sql
CREATE TABLE tmp_cities AS SELECT DISTINCT city FROM customers;
SELECT * FROM tmp_cities;
DROP TABLE tmp_cities;
```

<!-- result -->
**Result:**

✔ CREATE OK

| city |
|---|
| Caracas |
| Valencia |
| Maracay |
| Barquisimeto |

*4 rows*

✔ DROP OK
<!-- /result -->

</details>
