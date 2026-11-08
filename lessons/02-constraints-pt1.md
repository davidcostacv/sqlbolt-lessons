# Lesson 2 — Queries with constraints (Part 1): filtering numbers

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_with_constraints · [← Prev](01-select-queries.md) · [Next →](03-constraints-pt2.md)

## The idea in plain words

`SELECT … FROM …` gives you **every** row. Most of the time you only want **some** rows:
"only the jobs that cost more than $100", "only cars from 2015 or newer".

That's what `WHERE` does. It's a **filter**: the database checks each row against your condition and keeps only the rows where it's true.

## Syntax

```sql norun
SELECT columns
FROM table
WHERE condition
  AND/OR another_condition;
```

### Operators for numbers

| Operator | Meaning | Example |
|---|---|---|
| `=` | equal | `year = 2015` |
| `!=` or `<>` | not equal | `year != 2015` |
| `<` `<=` `>` `>=` | smaller / bigger | `parts_cost > 100` |
| `BETWEEN a AND b` | inside the range (**includes** a and b) | `year BETWEEN 2010 AND 2015` |
| `NOT BETWEEN a AND b` | outside the range | `year NOT BETWEEN 2010 AND 2015` |
| `IN (a, b, c)` | is one of the list | `id IN (1, 3, 5)` |
| `NOT IN (a, b, c)` | is none of the list | `id NOT IN (1, 3, 5)` |

- `AND` → **both** conditions must be true
- `OR` → **at least one** must be true

## Practical examples

Jobs where the parts cost more than $100:

```sql
SELECT id, service, parts_cost
FROM jobs
WHERE parts_cost > 100;
```

<!-- result -->
**Result:**

| id | service | parts_cost |
|---|---|---|
| 3 | Injector replacement | 320.0 |
| 4 | Alternator repair | 150.0 |
| 5 | Brake discs | 140.0 |
| 6 | Fuel pump | 210.0 |
| 9 | Starter motor | 180.0 |
| 11 | Injector replacement | 360.0 |

*6 rows*
<!-- /result -->

Cars made between 2010 and 2015 (both years included):

```sql
SELECT make, model, year
FROM cars
WHERE year BETWEEN 2010 AND 2015;
```

<!-- result -->
**Result:**

| make | model | year |
|---|---|---|
| Toyota | Corolla | 2015 |
| Ford | Explorer | 2012 |
| Chevrolet | Aveo | 2010 |
| Hyundai | Accent | 2014 |
| Ford | Fiesta | 2011 |

*5 rows*
<!-- /result -->

Specific cars by their id, using a list:

```sql
SELECT id, make, model
FROM cars
WHERE id IN (1, 4, 7);
```

<!-- result -->
**Result:**

| id | make | model |
|---|---|---|
| 1 | Toyota | Corolla |
| 4 | Toyota | Hilux |
| 7 | Toyota | Fortuner |

*3 rows*
<!-- /result -->

Two conditions at once — long jobs (3+ hours) **and** expensive parts (over $200):

```sql
SELECT service, labor_hours, parts_cost
FROM jobs
WHERE labor_hours >= 3
  AND parts_cost > 200;
```

<!-- result -->
**Result:**

| service | labor_hours | parts_cost |
|---|---|---|
| Injector replacement | 4.0 | 320.0 |
| Fuel pump | 3.5 | 210.0 |
| Injector replacement | 4.5 | 360.0 |

*3 rows*
<!-- /result -->

`OR` — free jobs (no parts) **or** very short ones:

```sql
SELECT service, labor_hours, parts_cost
FROM jobs
WHERE parts_cost = 0
   OR labor_hours < 1;
```

<!-- result -->
**Result:**

| service | labor_hours | parts_cost |
|---|---|---|
| Battery check | 0.5 | 0.0 |
| Engine scan | 1.0 | 0.0 |
| Oil leak check | 1.0 | 0.0 |

*3 rows*
<!-- /result -->

## Common mistakes

- **Mixing `AND` and `OR` without parentheses.** `AND` is evaluated first, like `×` before `+` in math. When in doubt, add `( )`:
  `WHERE status = 'done' AND (parts_cost > 200 OR labor_hours > 3)`
- **`BETWEEN 2015 AND 2010`** (big number first) returns nothing. Always small → big.
- **Using `==`** — in SQL equality is a single `=`.

## Practice

1. Jobs with `labor_hours` of exactly 2.
2. Cars older than 2012 (year less than 2012).
3. Mechanics who charge between $16 and $21 per hour.
4. Jobs whose id is NOT 1, 2 or 3 and that cost less than $50 in parts.

<details><summary>Answers</summary>

```sql
SELECT * FROM jobs WHERE labor_hours = 2;
```

<!-- result -->
**Result:**

| id | car_id | mechanic_id | service | labor_hours | parts_cost | opened_on | status |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 1 | Injector cleaning | 2.0 | 35.0 | 2025-01-12 | done |
| 8 | 8 | 1 | Injector cleaning | 2.0 | 35.0 | 2025-08-09 | done |

*2 rows*
<!-- /result -->

```sql
SELECT make, model, year FROM cars WHERE year < 2012;
```

<!-- result -->
**Result:**

| make | model | year |
|---|---|---|
| Chevrolet | Aveo | 2010 |
| Ford | Fiesta | 2011 |
| Chevrolet | Optra | 2008 |
| Mitsubishi | Lancer | 2009 |

*4 rows*
<!-- /result -->

```sql
SELECT name, hourly_rate FROM mechanics WHERE hourly_rate BETWEEN 16 AND 21;
```

<!-- result -->
**Result:**

| name | hourly_rate |
|---|---|
| Ramon Diaz | 18.0 |
| Elena Castro | 20.0 |

*2 rows*
<!-- /result -->

```sql
SELECT id, service, parts_cost
FROM jobs
WHERE id NOT IN (1, 2, 3)
  AND parts_cost < 50;
```

<!-- result -->
**Result:**

| id | service | parts_cost |
|---|---|---|
| 7 | Battery check | 0.0 |
| 8 | Injector cleaning | 35.0 |
| 10 | Brake fluid flush | 20.0 |
| 12 | Headlight wiring | 25.0 |
| 13 | Engine scan | 0.0 |
| 14 | Oil leak check | 0.0 |
| 15 | Fuel filter | 45.0 |

*7 rows*
<!-- /result -->

</details>
