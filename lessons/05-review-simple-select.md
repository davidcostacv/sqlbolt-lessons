# Lesson 5 — Review: simple SELECT queries

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_review · [← Prev](04-filtering-sorting.md) · [Next →](06-joins.md)

## What you know so far

```sql norun
SELECT DISTINCT column, another_column   -- 1. what columns
FROM table                               -- 2. from where
WHERE condition AND/OR condition         -- 3. which rows
ORDER BY column ASC/DESC                 -- 4. in what order
LIMIT n OFFSET m;                        -- 5. how many
```

That one shape answers a surprising number of real questions. Read every query like a sentence:
*"Give me X, from Y, only where Z, sorted by W, just N of them."*

## Practical examples — real workshop questions

**"Which open or in-progress jobs do we have, oldest first?"** (what the boss asks every morning)

```sql
SELECT id, service, status, opened_on
FROM jobs
WHERE status IN ('open', 'in progress')
ORDER BY opened_on ASC;
```

<!-- result -->
**Result:**

| id | service | status | opened_on |
|---|---|---|---|
| 11 | Injector replacement | in progress | 2025-10-25 |
| 12 | Headlight wiring | in progress | 2025-11-01 |
| 13 | Engine scan | open | 2025-11-03 |
| 14 | Oil leak check | open | 2025-11-04 |
| 15 | Fuel filter | in progress | 2025-11-05 |

*5 rows*
<!-- /result -->

**"Which Toyotas do we work on, newest model first?"**

```sql
SELECT model, year, plate
FROM cars
WHERE make = 'Toyota'
ORDER BY year DESC;
```

<!-- result -->
**Result:**

| model | year | plate |
|---|---|---|
| Fortuner | 2020 | EF963GH |
| Hilux | 2018 | PQ321RS |
| Corolla | 2015 | AB123CD |

*3 rows*
<!-- /result -->

**"Who are our 3 most recent customers in Caracas?"**

```sql
SELECT name, joined_on
FROM customers
WHERE city = 'Caracas'
ORDER BY joined_on DESC
LIMIT 3;
```

<!-- result -->
**Result:**

| name | joined_on |
|---|---|
| Miguel Torres | 2025-04-22 |
| Sofia Pineda | 2024-03-30 |
| Carla Ortega | 2023-09-21 |

*3 rows*
<!-- /result -->

**"Customers we can't call"** (missing phone — sneak peek of Lesson 8):

```sql
SELECT name, city FROM customers WHERE phone IS NULL;
```

<!-- result -->
**Result:**

| name | city |
|---|---|
| Carla Ortega | Caracas |
| Jorge Luna | Barquisimeto |

*2 rows*
<!-- /result -->

**"Injector jobs that took 3+ hours, most expensive first"**

```sql
SELECT service, labor_hours, parts_cost
FROM jobs
WHERE service LIKE '%injector%'
  AND labor_hours >= 3
ORDER BY parts_cost DESC;
```

<!-- result -->
**Result:**

| service | labor_hours | parts_cost |
|---|---|---|
| Injector replacement | 4.5 | 360.0 |
| Injector replacement | 4.0 | 320.0 |

*2 rows*
<!-- /result -->

## Practice

1. All distinct car makes, A→Z.
2. The 2 oldest cars in the workshop.
3. Jobs opened in 2025-10 or later (dates are text `'YYYY-MM-DD'`, so `>= '2025-10-01'` works!).
4. Customers from Valencia or Maracay, sorted by name.
5. The second most expensive job in parts (hint: `LIMIT 1 OFFSET 1`).

<details><summary>Answers</summary>

```sql
SELECT DISTINCT make FROM cars ORDER BY make;
```

<!-- result -->
**Result:**

| make |
|---|
| Chevrolet |
| Ford |
| Hyundai |
| Kia |
| Mitsubishi |
| Toyota |

*6 rows*
<!-- /result -->

```sql
SELECT make, model, year FROM cars ORDER BY year ASC LIMIT 2;
```

<!-- result -->
**Result:**

| make | model | year |
|---|---|---|
| Chevrolet | Optra | 2008 |
| Mitsubishi | Lancer | 2009 |

*2 rows*
<!-- /result -->

```sql
SELECT id, service, opened_on FROM jobs WHERE opened_on >= '2025-10-01' ORDER BY opened_on;
```

<!-- result -->
**Result:**

| id | service | opened_on |
|---|---|---|
| 10 | Brake fluid flush | 2025-10-02 |
| 11 | Injector replacement | 2025-10-25 |
| 12 | Headlight wiring | 2025-11-01 |
| 13 | Engine scan | 2025-11-03 |
| 14 | Oil leak check | 2025-11-04 |
| 15 | Fuel filter | 2025-11-05 |

*6 rows*
<!-- /result -->

```sql
SELECT name, city FROM customers WHERE city IN ('Valencia', 'Maracay') ORDER BY name;
```

<!-- result -->
**Result:**

| name | city |
|---|---|
| Luis Mendoza | Valencia |
| Pedro Salas | Maracay |
| Valeria Campos | Valencia |

*3 rows*
<!-- /result -->

```sql
SELECT service, parts_cost FROM jobs ORDER BY parts_cost DESC LIMIT 1 OFFSET 1;
```

<!-- result -->
**Result:**

| service | parts_cost |
|---|---|
| Injector replacement | 320.0 |

*1 row*
<!-- /result -->

</details>

> 💡 Why does comparing dates as text work? Because `'YYYY-MM-DD'` sorts alphabetically in the same order as time. That's why storing dates this way is a good habit. `'10/02/2025'` would **not** sort correctly.
