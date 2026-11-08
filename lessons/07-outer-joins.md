# Lesson 7 — OUTER JOINs

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_with_outer_joins · [← Prev](06-joins.md) · [Next →](08-nulls.md)

## The idea in plain words

`INNER JOIN` throws away rows that have no partner. Sometimes those rows are exactly what you care about:

- *"Which customers have **no** car registered?"*
- *"Which jobs have **nobody** assigned?"*
- *"Which mechanic has **no** work yet?"*

**OUTER** joins keep the rows without a match and fill the missing side with `NULL` ("no value" — see Lesson 8).

| Join | Keeps |
|---|---|
| `INNER JOIN` | only rows that match on both sides |
| `LEFT JOIN` | **all** rows from the left table (the one in `FROM`) + matches from the right |
| `RIGHT JOIN` | **all** rows from the right table + matches from the left |
| `FULL JOIN` | **all** rows from both sides |

`LEFT JOIN` is by far the most used. A `RIGHT JOIN` is just a `LEFT JOIN` with the tables swapped, so many people never use it.

## Syntax

```sql norun
SELECT columns
FROM left_table
LEFT JOIN right_table
    ON left_table.id = right_table.left_id;
```

## Practical examples

Every customer with their cars — **including** customers with no car:

```sql
SELECT cu.name, c.make, c.model
FROM customers AS cu
LEFT JOIN cars AS c ON c.customer_id = cu.id
ORDER BY cu.id;
```

<!-- result -->
**Result:**

| name | make | model |
|---|---|---|
| Ana Rivas | Ford | Explorer |
| Ana Rivas | Toyota | Corolla |
| Luis Mendoza | Chevrolet | Aveo |
| Carla Ortega | Toyota | Hilux |
| Pedro Salas | Hyundai | Accent |
| Sofia Pineda | Ford | Fiesta |
| Sofia Pineda | Toyota | Fortuner |
| Jorge Luna | Chevrolet | Optra |
| Valeria Campos | Kia | Rio |
| Valeria Campos | Mitsubishi | Lancer |
| Miguel Torres | NULL | NULL |

*11 rows*
<!-- /result -->

Look at the last row: Miguel Torres has `NULL` make and model. With an `INNER JOIN` he'd be gone.

Now the classic trick: **find the rows without a match** — keep only the ones where the right side is NULL:

```sql
SELECT cu.name
FROM customers AS cu
LEFT JOIN cars AS c ON c.customer_id = cu.id
WHERE c.id IS NULL;
```

<!-- result -->
**Result:**

| name |
|---|
| Miguel Torres |

*1 row*
<!-- /result -->

All jobs with their mechanic, even unassigned ones:

```sql
SELECT j.id, j.service, m.name AS mechanic
FROM jobs AS j
LEFT JOIN mechanics AS m ON j.mechanic_id = m.id
WHERE j.status != 'done';
```

<!-- result -->
**Result:**

| id | service | mechanic |
|---|---|---|
| 11 | Injector replacement | Ramon Diaz |
| 12 | Headlight wiring | Elena Castro |
| 13 | Engine scan | NULL |
| 14 | Oil leak check | NULL |
| 15 | Fuel filter | Ramon Diaz |

*5 rows*
<!-- /result -->

Which mechanic has no jobs at all?

```sql
SELECT m.name, m.specialty
FROM mechanics AS m
LEFT JOIN jobs AS j ON j.mechanic_id = m.id
WHERE j.id IS NULL;
```

<!-- result -->
**Result:**

| name | specialty |
|---|---|
| Lucia Morales | Diagnostics |

*1 row*
<!-- /result -->

`FULL JOIN` — mechanics and jobs, showing **both** the idle mechanic and the unassigned jobs:

```sql
SELECT m.name AS mechanic, j.id AS job, j.service
FROM mechanics AS m
FULL JOIN jobs AS j ON j.mechanic_id = m.id
WHERE m.id IS NULL OR j.id IS NULL;
```

<!-- result -->
**Result:**

| mechanic | job | service |
|---|---|---|
| Lucia Morales | NULL | NULL |
| NULL | 13 | Engine scan |
| NULL | 14 | Oil leak check |

*3 rows*
<!-- /result -->

## Common mistakes

- **Filtering the right table in `WHERE`** cancels the LEFT JOIN. `LEFT JOIN cars c … WHERE c.make = 'Toyota'` removes Miguel again, because `NULL = 'Toyota'` is not true. If you want "all customers + only their Toyotas", put the filter in the `ON`:
  `LEFT JOIN cars c ON c.customer_id = cu.id AND c.make = 'Toyota'`
- **Using `= NULL`** instead of `IS NULL` (next lesson explains why).

## Practice

1. Every car with the number of the job(s) done on it — including cars with no jobs. (Do any cars have no jobs?)
2. List only the jobs that have **no** mechanic.
3. All customers and their cars, but only show Toyota cars (customers without Toyotas should still appear with NULL).

<details><summary>Answers</summary>

```sql
SELECT c.plate, c.model, j.id AS job_id
FROM cars AS c
LEFT JOIN jobs AS j ON j.car_id = c.id
ORDER BY c.id;
```

<!-- result -->
**Result:**

| plate | model | job_id |
|---|---|---|
| AB123CD | Corolla | 1 |
| AB123CD | Corolla | 10 |
| XY987ZT | Explorer | 4 |
| KL456MN | Aveo | 2 |
| KL456MN | Aveo | 12 |
| PQ321RS | Hilux | 3 |
| PQ321RS | Hilux | 15 |
| GH741JK | Accent | 5 |
| GH741JK | Accent | 14 |
| TU852VW | Fiesta | 6 |
| EF963GH | Fortuner | 7 |
| EF963GH | Fortuner | 13 |
| MN159OP | Optra | 8 |
| QR357ST | Rio | 9 |
| UV246WX | Lancer | 11 |

*15 rows*
<!-- /result -->

Every car has at least one job, so no NULLs here — that's an answer too!

```sql
SELECT id, service FROM jobs WHERE mechanic_id IS NULL;
```

<!-- result -->
**Result:**

| id | service |
|---|---|
| 13 | Engine scan |
| 14 | Oil leak check |

*2 rows*
<!-- /result -->

```sql
SELECT cu.name, c.model
FROM customers AS cu
LEFT JOIN cars AS c ON c.customer_id = cu.id AND c.make = 'Toyota'
ORDER BY cu.id;
```

<!-- result -->
**Result:**

| name | model |
|---|---|
| Ana Rivas | Corolla |
| Luis Mendoza | NULL |
| Carla Ortega | Hilux |
| Pedro Salas | NULL |
| Sofia Pineda | Fortuner |
| Jorge Luna | NULL |
| Valeria Campos | NULL |
| Miguel Torres | NULL |

*8 rows*
<!-- /result -->

</details>
