# Lesson 12 — Order of execution of a query

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_order_of_execution · [← Prev](11-aggregates-pt2.md) · [Next →](13-inserting-rows.md)

## The idea in plain words

You **write** a query in this order:

```sql norun
SELECT DISTINCT … FROM … JOIN … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT …
```

But the database **runs** it in a different order. Knowing the real order explains almost every "why doesn't this work?" moment.

| Step | Clause | What happens |
|---|---|---|
| 1 | `FROM` + `JOIN` | build the big working table (all tables glued together) |
| 2 | `WHERE` | throw away rows that don't pass |
| 3 | `GROUP BY` | put remaining rows into groups |
| 4 | `HAVING` | throw away groups that don't pass |
| 5 | `SELECT` | calculate the output columns (and their aliases) |
| 6 | `DISTINCT` | remove duplicate output rows |
| 7 | `ORDER BY` | sort |
| 8 | `LIMIT` / `OFFSET` | cut the final list |

A kitchen analogy: grab all ingredients (FROM/JOIN) → throw out the bad ones (WHERE) → sort them into bowls (GROUP BY) → discard bowls you don't need (HAVING) → cook and plate (SELECT) → arrange the plates (ORDER BY) → serve only N plates (LIMIT).

## What this explains

**1. Why `WHERE` can't use aggregates** — at step 2 no grouping has happened yet (that's why `HAVING` exists).

**2. Why `WHERE` can't use a `SELECT` alias** (in standard SQL) — the alias is created at step 5, after `WHERE` at step 2. Repeat the formula instead. (SQLite is lenient and lets you do it anyway, but PostgreSQL, MySQL and most others don't — so don't get used to it.)

**3. Why `ORDER BY` *can* use aliases** — step 7 runs after step 5, so the alias already exists:

```sql
SELECT service, labor_hours * 20 AS estimate
FROM jobs
ORDER BY estimate DESC
LIMIT 3;
```

<!-- result -->
**Result:**

| service | estimate |
|---|---|
| Injector replacement | 90.0 |
| Injector replacement | 80.0 |
| Fuel pump | 70.0 |

*3 rows*
<!-- /result -->

**4. Why `LIMIT` gives "top N"** — it's the very last step, after sorting.

## A full query, step by step

*"Top 2 mechanics by revenue (labor + parts) on finished jobs, only if they made over $300"*

```sql
SELECT m.name,                                                   -- 5
       SUM(j.labor_hours * m.hourly_rate + j.parts_cost) AS revenue
FROM jobs AS j                                                   -- 1
JOIN mechanics AS m ON j.mechanic_id = m.id                      -- 1
WHERE j.status = 'done'                                          -- 2
GROUP BY m.name                                                  -- 3
HAVING revenue > 300                                             -- 4
ORDER BY revenue DESC                                            -- 7
LIMIT 2;                                                         -- 8
```

<!-- result -->
**Result:**

| name | revenue |
|---|---|
| Ramon Diaz | 807.0 |
| Elena Castro | 450.0 |

*2 rows*
<!-- /result -->

Read it in the numbered order and you can predict the result before running it:
1. join jobs with mechanics (unassigned jobs drop out — inner join),
2. keep only `done` jobs,
3. one group per mechanic,
4. keep mechanics over $300,
5. compute name + revenue,
7. sort high → low,
8. keep 2.

> SQLite is friendly and lets `HAVING` use the `revenue` alias. Not every database does — if you get an error elsewhere, repeat the `SUM(...)`.

## Practice

Without running it first, predict how many rows this returns, then run it:

```sql
SELECT city, COUNT(*) AS n
FROM customers
WHERE joined_on >= '2024-01-01'
GROUP BY city
HAVING COUNT(*) >= 1
ORDER BY n DESC
LIMIT 10;
```

<!-- result -->
**Result:**

| city | n |
|---|---|
| Caracas | 2 |
| Valencia | 1 |
| Maracay | 1 |
| Barquisimeto | 1 |

*4 rows*
<!-- /result -->

<details><summary>Explanation</summary>

Customers who joined in 2024 or later: Pedro (Maracay), Sofia (Caracas), Jorge (Barquisimeto), Valeria (Valencia), Miguel (Caracas). Grouped by city → Caracas 2, Maracay 1, Barquisimeto 1, Valencia 1. All groups have ≥ 1, so 4 rows. `LIMIT 10` doesn't cut anything.

</details>
