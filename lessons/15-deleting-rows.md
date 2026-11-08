# Lesson 15 — Deleting rows

📘 SQLBolt: https://sqlbolt.com/lesson/deleting_rows · [← Prev](14-updating-rows.md) · [Next →](16-creating-tables.md)

## The idea in plain words

`DELETE` removes whole rows. Same danger as `UPDATE`: **without `WHERE`, it deletes everything** in the table.

```sql norun
DELETE FROM table
WHERE condition;
```

Same safe habit:
1. `SELECT * FROM table WHERE condition;` → look at what will go.
2. Count it. Is it the number you expected?
3. Only then change `SELECT *` into `DELETE`.

## Practical examples

We want to delete job 14 (the oil leak check was cancelled). Look first:

```sql
SELECT id, service, status FROM jobs WHERE id = 14;
```

<!-- result -->
**Result:**

| id | service | status |
|---|---|---|
| 14 | Oil leak check | open |

*1 row*
<!-- /result -->

Exactly one row, the right one. Delete it:

```sql
DELETE FROM jobs WHERE id = 14;
```

<!-- result -->
**Result:**

✔ DELETE OK — 1 row affected
<!-- /result -->

Delete with a condition that could match several rows — all `open` jobs nobody was assigned to. Count first:

```sql
SELECT COUNT(*) AS will_delete FROM jobs WHERE status = 'open' AND mechanic_id IS NULL;
```

<!-- result -->
**Result:**

| will_delete |
|---|
| 1 |

*1 row*
<!-- /result -->

```sql
DELETE FROM jobs WHERE status = 'open' AND mechanic_id IS NULL;
```

<!-- result -->
**Result:**

✔ DELETE OK — 1 row affected
<!-- /result -->

## Foreign keys protect you

Can we delete Ana (customer 1)? She has 2 cars pointing at her. The database refuses, because those cars would point to nobody:

```sql error
DELETE FROM customers WHERE id = 1;
```

<!-- result -->
**Result:**

❌ Error: `FOREIGN KEY constraint failed`
<!-- /result -->

Miguel (customer 8) has no cars, so he can be deleted:

```sql
DELETE FROM customers WHERE id = 8;
```

<!-- result -->
**Result:**

✔ DELETE OK — 1 row affected
<!-- /result -->

To remove Ana for real you'd delete in order, **children first**: her jobs → her cars → her.

```sql
DELETE FROM jobs WHERE car_id IN (SELECT id FROM cars WHERE customer_id = 1);
DELETE FROM cars WHERE customer_id = 1;
DELETE FROM customers WHERE id = 1;
```

<!-- result -->
**Result:**

✔ DELETE OK — 3 rows affected

✔ DELETE OK — 2 rows affected

✔ DELETE OK — 1 row affected
<!-- /result -->

(`IN (SELECT …)` is a **subquery**: a query inside a query. There's more about them in [Lesson X](19-to-infinity-and-beyond.md).)

## Delete or "soft delete"?

In real apps people often **don't** delete. They add a column like `status = 'cancelled'` or `deleted_at` and filter it out. That way you keep history and can undo mistakes. Delete for real only when the data is truly useless or the law requires it.

## Practice

1. Delete all jobs that cost $0 in parts **and** are done. (Count first!)
2. Try to delete mechanic 1 (Ramon). What happens and why?
3. Delete mechanic 4 (Lucia) — why does this one work?

<details><summary>Answers</summary>

```sql
SELECT COUNT(*) FROM jobs WHERE parts_cost = 0 AND status = 'done';
```

<!-- result -->
**Result:**

| COUNT(*) |
|---|
| 1 |

*1 row*
<!-- /result -->

```sql
DELETE FROM jobs WHERE parts_cost = 0 AND status = 'done';
```

<!-- result -->
**Result:**

✔ DELETE OK — 1 row affected
<!-- /result -->

```sql error
DELETE FROM mechanics WHERE id = 1;
```

<!-- result -->
**Result:**

❌ Error: `FOREIGN KEY constraint failed`
<!-- /result -->

Ramon has jobs pointing at him (`jobs.mechanic_id = 1`), so the foreign key blocks it.

```sql
DELETE FROM mechanics WHERE id = 4;
```

<!-- result -->
**Result:**

✔ DELETE OK — 1 row affected
<!-- /result -->

Lucia has no jobs, nothing points to her, so she can go.

</details>
