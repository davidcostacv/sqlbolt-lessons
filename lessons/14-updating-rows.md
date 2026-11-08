# Lesson 14 — Updating rows

📘 SQLBolt: https://sqlbolt.com/lesson/updating_rows · [← Prev](13-inserting-rows.md) · [Next →](15-deleting-rows.md)

## The idea in plain words

`UPDATE` changes values in rows that already exist: a customer changes phone, a job moves from `open` to `done`, mechanics get a raise.

It has two parts:
- `SET` → **what** to change
- `WHERE` → **which rows** to change

> ⚠️ **The most dangerous mistake in SQL:** forgetting the `WHERE`. `UPDATE customers SET phone = '…'` with no WHERE changes **every customer's** phone. There's no "undo".

## Syntax

```sql norun
UPDATE table
SET column1 = value1,
    column2 = value2
WHERE condition;
```

## The safe habit: SELECT first, UPDATE second

1. Write the `WHERE` as a `SELECT` and look at the rows.
2. If it's exactly the rows you want, change `SELECT … FROM` into `UPDATE … SET`.

Step 1 — which jobs are we about to close?

```sql
SELECT id, service, status FROM jobs WHERE id = 12;
```

<!-- result -->
**Result:**

| id | service | status |
|---|---|---|
| 12 | Headlight wiring | in progress |

*1 row*
<!-- /result -->

Step 2 — close it:

```sql
UPDATE jobs SET status = 'done' WHERE id = 12;
```

<!-- result -->
**Result:**

✔ UPDATE OK — 1 row affected
<!-- /result -->

## Practical examples

Carla finally gave us her phone:

```sql
UPDATE customers
SET phone = '0412-555-0103'
WHERE id = 3;
```

<!-- result -->
**Result:**

✔ UPDATE OK — 1 row affected
<!-- /result -->

Assign the two unassigned jobs to Lucia (mechanic 4) and mark them in progress — two columns at once:

```sql
UPDATE jobs
SET mechanic_id = 4,
    status = 'in progress'
WHERE mechanic_id IS NULL;
```

<!-- result -->
**Result:**

✔ UPDATE OK — 2 rows affected
<!-- /result -->

```sql
SELECT id, service, mechanic_id, status FROM jobs WHERE mechanic_id = 4;
```

<!-- result -->
**Result:**

| id | service | mechanic_id | status |
|---|---|---|---|
| 13 | Engine scan | 4 | in progress |
| 14 | Oil leak check | 4 | in progress |

*2 rows*
<!-- /result -->

Use the current value in the new value — 10% raise for everyone hired before 2021:

```sql
UPDATE mechanics
SET hourly_rate = ROUND(hourly_rate * 1.10, 2)
WHERE hired_on < '2021-01-01';
```

<!-- result -->
**Result:**

✔ UPDATE OK — 2 rows affected
<!-- /result -->

```sql
SELECT name, hourly_rate, hired_on FROM mechanics;
```

<!-- result -->
**Result:**

| name | hourly_rate | hired_on |
|---|---|---|
| Ramon Diaz | 19.8 | 2019-05-01 |
| Elena Castro | 22.0 | 2020-08-15 |
| Tomas Herrera | 15.0 | 2022-02-01 |
| Lucia Morales | 22.0 | 2025-09-01 |

*4 rows*
<!-- /result -->

Rename a service everywhere it appears (here it's only one row, but the same query would fix a thousand):

```sql
UPDATE jobs
SET service = 'Brake fluid replacement'
WHERE service = 'Brake fluid flush';
```

<!-- result -->
**Result:**

✔ UPDATE OK — 1 row affected
<!-- /result -->

## Common mistakes

- **No `WHERE`** → every row changes. Always run the `SELECT` first.
- **`WHERE id = 3` on the wrong table** → you just edited a car instead of a customer.
- **Updating with `= NULL` in the WHERE** → matches nothing. Use `IS NULL` (Lesson 8).

## Practice

1. Valeria Campos moved to Caracas. Update her city.
2. Mark every `in progress` job as `done`.
3. Add $5 to the parts cost of every injector job.

<details><summary>Answers</summary>

```sql
UPDATE customers SET city = 'Caracas' WHERE name = 'Valeria Campos';
```

<!-- result -->
**Result:**

✔ UPDATE OK — 1 row affected
<!-- /result -->

```sql
UPDATE jobs SET status = 'done' WHERE status = 'in progress';
```

<!-- result -->
**Result:**

✔ UPDATE OK — 4 rows affected
<!-- /result -->

```sql
UPDATE jobs SET parts_cost = parts_cost + 5 WHERE service LIKE '%injector%';
```

<!-- result -->
**Result:**

✔ UPDATE OK — 4 rows affected
<!-- /result -->

</details>
