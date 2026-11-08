# Lesson 8 — A short note on NULLs

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_with_nulls · [← Prev](07-outer-joins.md) · [Next →](09-expressions.md)

## The idea in plain words

`NULL` means **"unknown / no value"**. It is **not** zero and **not** an empty text `''`.

- Carla's phone is `NULL` → we don't know it. That's different from a phone of `''`.
- Job 13's `mechanic_id` is `NULL` → nobody assigned yet.

The weird part: **NULL is never equal to anything — not even to another NULL.**
`NULL = NULL` is not true, it's *unknown*. So `WHERE phone = NULL` returns **nothing**, always.

To test for NULL you must use special operators:

```sql norun
WHERE column IS NULL
WHERE column IS NOT NULL
```

## Practical examples

The trap — this looks right but returns no rows:

```sql
SELECT name FROM customers WHERE phone = NULL;
```

<!-- result -->
**Result:**

*(no rows)*
<!-- /result -->

The correct way:

```sql
SELECT name FROM customers WHERE phone IS NULL;
```

<!-- result -->
**Result:**

| name |
|---|
| Carla Ortega |
| Jorge Luna |

*2 rows*
<!-- /result -->

Customers we **can** call:

```sql
SELECT name, phone FROM customers WHERE phone IS NOT NULL;
```

<!-- result -->
**Result:**

| name | phone |
|---|---|
| Ana Rivas | 0414-555-0101 |
| Luis Mendoza | 0424-555-0102 |
| Pedro Salas | 0412-555-0104 |
| Sofia Pineda | 0416-555-0105 |
| Valeria Campos | 0414-555-0107 |
| Miguel Torres | 0426-555-0108 |

*6 rows*
<!-- /result -->

Show something nicer than NULL with `COALESCE(value, fallback)` — it returns the first non-NULL value:

```sql
SELECT name, COALESCE(phone, 'no phone') AS phone
FROM customers;
```

<!-- result -->
**Result:**

| name | phone |
|---|---|
| Ana Rivas | 0414-555-0101 |
| Luis Mendoza | 0424-555-0102 |
| Carla Ortega | no phone |
| Pedro Salas | 0412-555-0104 |
| Sofia Pineda | 0416-555-0105 |
| Jorge Luna | no phone |
| Valeria Campos | 0414-555-0107 |
| Miguel Torres | 0426-555-0108 |

*8 rows*
<!-- /result -->

`NULL` spreads in math: anything `+ NULL` is `NULL`.

```sql
SELECT 5 + NULL AS result;
```

<!-- result -->
**Result:**

| result |
|---|
| NULL |

*1 row*
<!-- /result -->

Another trap: `!=` also skips NULLs. "Jobs **not** assigned to Ramon (id 1)" — the unassigned ones vanish:

```sql
SELECT id, service, mechanic_id FROM jobs WHERE mechanic_id != 1;
```

<!-- result -->
**Result:**

| id | service | mechanic_id |
|---|---|---|
| 2 | Brake pads | 3 |
| 4 | Alternator repair | 2 |
| 5 | Brake discs | 3 |
| 7 | Battery check | 2 |
| 9 | Starter motor | 2 |
| 10 | Brake fluid flush | 3 |
| 12 | Headlight wiring | 2 |

*7 rows*
<!-- /result -->

Jobs 13 and 14 aren't there! You have to ask for them explicitly:

```sql
SELECT id, service, mechanic_id
FROM jobs
WHERE mechanic_id != 1 OR mechanic_id IS NULL;
```

<!-- result -->
**Result:**

| id | service | mechanic_id |
|---|---|---|
| 2 | Brake pads | 3 |
| 4 | Alternator repair | 2 |
| 5 | Brake discs | 3 |
| 7 | Battery check | 2 |
| 9 | Starter motor | 2 |
| 10 | Brake fluid flush | 3 |
| 12 | Headlight wiring | 2 |
| 13 | Engine scan | NULL |
| 14 | Oil leak check | NULL |

*9 rows*
<!-- /result -->

## When to avoid NULL

When you design a table (Lesson 16), it's often better to prevent NULLs with `NOT NULL` or use a sensible default (`0`, `'open'`), so you don't need these checks everywhere. Use NULL only when "unknown" is a real, meaningful state.

## Practice

1. List jobs that **have** a mechanic assigned.
2. Show every job with its mechanic id, but print `0` instead of NULL.
3. Count how many customers have no phone (peek ahead: `SELECT COUNT(*) …`).

<details><summary>Answers</summary>

```sql
SELECT id, service FROM jobs WHERE mechanic_id IS NOT NULL;
```

<!-- result -->
**Result:**

| id | service |
|---|---|
| 1 | Injector cleaning |
| 2 | Brake pads |
| 3 | Injector replacement |
| 4 | Alternator repair |
| 5 | Brake discs |
| 6 | Fuel pump |
| 7 | Battery check |
| 8 | Injector cleaning |
| 9 | Starter motor |
| 10 | Brake fluid flush |
| 11 | Injector replacement |
| 12 | Headlight wiring |
| 15 | Fuel filter |

*13 rows*
<!-- /result -->

```sql
SELECT id, service, COALESCE(mechanic_id, 0) AS mechanic_id FROM jobs;
```

<!-- result -->
**Result:**

| id | service | mechanic_id |
|---|---|---|
| 1 | Injector cleaning | 1 |
| 2 | Brake pads | 3 |
| 3 | Injector replacement | 1 |
| 4 | Alternator repair | 2 |
| 5 | Brake discs | 3 |
| 6 | Fuel pump | 1 |
| 7 | Battery check | 2 |
| 8 | Injector cleaning | 1 |
| 9 | Starter motor | 2 |
| 10 | Brake fluid flush | 3 |
| 11 | Injector replacement | 1 |
| 12 | Headlight wiring | 2 |
| 13 | Engine scan | 0 |
| 14 | Oil leak check | 0 |
| 15 | Fuel filter | 1 |

*15 rows*
<!-- /result -->

```sql
SELECT COUNT(*) AS without_phone FROM customers WHERE phone IS NULL;
```

<!-- result -->
**Result:**

| without_phone |
|---|
| 2 |

*1 row*
<!-- /result -->

</details>
