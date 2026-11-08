# Lesson 3 — Queries with constraints (Part 2): filtering text

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_with_constraints_pt_2 · [← Prev](02-constraints-pt1.md) · [Next →](04-filtering-sorting.md)

## The idea in plain words

Same `WHERE` as last lesson, but now the column holds **text** (names, cities, services).
Two big rules:

1. Text values go between **single quotes**: `'Caracas'` ✅ — `Caracas` ❌ (SQL would think it's a column name).
2. For "contains / starts with / ends with" you use `LIKE` with **wildcards**.

## Syntax

| Operator | Meaning | Example |
|---|---|---|
| `=` | exactly equal | `city = 'Caracas'` |
| `!=` or `<>` | not equal | `city != 'Caracas'` |
| `LIKE` | matches a pattern | `service LIKE 'Brake%'` |
| `NOT LIKE` | does not match | `service NOT LIKE '%Injector%'` |
| `IN ('a','b')` | one of the list | `city IN ('Valencia', 'Maracay')` |
| `NOT IN ('a','b')` | none of the list | `city NOT IN ('Caracas')` |

### Wildcards inside `LIKE`

| Wildcard | Means | Pattern | Matches |
|---|---|---|---|
| `%` | any amount of characters (even zero) | `'Brake%'` | Brake pads, Brake discs, Brake fluid flush |
| `_` | exactly **one** character | `'_ia'` | Kia (3 letters ending in "ia") |

In SQLite, `LIKE` ignores upper/lower case for normal letters (`'toyota'` matches `'Toyota'`). In other databases (like PostgreSQL) it does care — there you'd use `ILIKE`.

## Practical examples

All customers from Caracas:

```sql
SELECT name, city FROM customers WHERE city = 'Caracas';
```

<!-- result -->
**Result:**

| name | city |
|---|---|
| Ana Rivas | Caracas |
| Carla Ortega | Caracas |
| Sofia Pineda | Caracas |
| Miguel Torres | Caracas |

*4 rows*
<!-- /result -->

Every brake-related job (service **starts with** "Brake"):

```sql
SELECT id, service FROM jobs WHERE service LIKE 'Brake%';
```

<!-- result -->
**Result:**

| id | service |
|---|---|
| 2 | Brake pads |
| 5 | Brake discs |
| 10 | Brake fluid flush |

*3 rows*
<!-- /result -->

Anything about injectors (the word appears **anywhere**):

```sql
SELECT id, service FROM jobs WHERE service LIKE '%injector%';
```

<!-- result -->
**Result:**

| id | service |
|---|---|
| 1 | Injector cleaning |
| 3 | Injector replacement |
| 8 | Injector cleaning |
| 11 | Injector replacement |

*4 rows*
<!-- /result -->

Customers outside the two biggest cities:

```sql
SELECT name, city FROM customers WHERE city NOT IN ('Caracas', 'Valencia');
```

<!-- result -->
**Result:**

| name | city |
|---|---|
| Pedro Salas | Maracay |
| Jorge Luna | Barquisimeto |

*2 rows*
<!-- /result -->

Car makes with exactly 3 letters, using `_` three times:

```sql
SELECT DISTINCT make FROM cars WHERE make LIKE '___';
```

<!-- result -->
**Result:**

| make |
|---|
| Kia |

*1 row*
<!-- /result -->

(`DISTINCT` removes repeated rows — you'll see it properly in the next lesson.)

## Common mistakes

- **Double quotes for text**: `city = "Caracas"`. SQLite accepts it (it guesses you meant text), but in standard SQL double quotes mean a column/table name — PostgreSQL would say "column Caracas does not exist". Always use single quotes for text.
- **`LIKE` without wildcards** is almost `=` (in SQLite it just ignores upper/lower case). `service LIKE 'Brake'` finds nothing, because no service is exactly "Brake".
- **Extra spaces**: `'Caracas '` (with a space) is not `'Caracas'`.

## Practice

1. Jobs whose status is `'done'`.
2. Customers whose name starts with "M".
3. Jobs that are **not** done (two ways: `!=` and `NOT IN`).
4. Cars whose plate ends in "CD".

<details><summary>Answers</summary>

```sql
SELECT id, service, status FROM jobs WHERE status = 'done';
```

<!-- result -->
**Result:**

| id | service | status |
|---|---|---|
| 1 | Injector cleaning | done |
| 2 | Brake pads | done |
| 3 | Injector replacement | done |
| 4 | Alternator repair | done |
| 5 | Brake discs | done |
| 6 | Fuel pump | done |
| 7 | Battery check | done |
| 8 | Injector cleaning | done |
| 9 | Starter motor | done |
| 10 | Brake fluid flush | done |

*10 rows*
<!-- /result -->

```sql
SELECT name FROM customers WHERE name LIKE 'M%';
```

<!-- result -->
**Result:**

| name |
|---|
| Miguel Torres |

*1 row*
<!-- /result -->

```sql
SELECT id, service, status FROM jobs WHERE status != 'done';
```

<!-- result -->
**Result:**

| id | service | status |
|---|---|---|
| 11 | Injector replacement | in progress |
| 12 | Headlight wiring | in progress |
| 13 | Engine scan | open |
| 14 | Oil leak check | open |
| 15 | Fuel filter | in progress |

*5 rows*
<!-- /result -->

```sql
SELECT id, service, status FROM jobs WHERE status NOT IN ('done');
```

<!-- result -->
**Result:**

| id | service | status |
|---|---|---|
| 11 | Injector replacement | in progress |
| 12 | Headlight wiring | in progress |
| 13 | Engine scan | open |
| 14 | Oil leak check | open |
| 15 | Fuel filter | in progress |

*5 rows*
<!-- /result -->

```sql
SELECT plate, make, model FROM cars WHERE plate LIKE '%CD';
```

<!-- result -->
**Result:**

| plate | make | model |
|---|---|---|
| AB123CD | Toyota | Corolla |

*1 row*
<!-- /result -->

</details>
