# Lesson 10 — Queries with aggregates (Part 1)

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_with_aggregates · [← Prev](09-expressions.md) · [Next →](11-aggregates-pt2.md)

## The idea in plain words

So far every query returned **one result row per table row**. Aggregates **squash many rows into one number**: a total, an average, a count.

| Function | Gives you |
|---|---|
| `COUNT(*)` | how many rows |
| `COUNT(column)` | how many rows where that column is **not NULL** |
| `SUM(column)` | the total |
| `AVG(column)` | the average |
| `MIN(column)` / `MAX(column)` | smallest / biggest |

Then `GROUP BY` lets you do it **per group**: not "total of all jobs" but "total **per mechanic**", "count **per city**". Think of it as a pivot table in Excel.

## Syntax

```sql norun
SELECT group_column, AGG_FUNC(column) AS name
FROM table
WHERE condition          -- filters rows BEFORE grouping
GROUP BY group_column;
```

## Practical examples

How many jobs do we have in total?

```sql
SELECT COUNT(*) AS total_jobs FROM jobs;
```

<!-- result -->
**Result:**

| total_jobs |
|---|
| 15 |

*1 row*
<!-- /result -->

`COUNT(*)` vs `COUNT(column)` — 15 jobs, but only 13 have a mechanic:

```sql
SELECT COUNT(*) AS all_jobs, COUNT(mechanic_id) AS assigned_jobs FROM jobs;
```

<!-- result -->
**Result:**

| all_jobs | assigned_jobs |
|---|---|
| 15 | 13 |

*1 row*
<!-- /result -->

Total, average, cheapest and most expensive parts bill:

```sql
SELECT SUM(parts_cost) AS total,
       ROUND(AVG(parts_cost), 2) AS average,
       MIN(parts_cost) AS cheapest,
       MAX(parts_cost) AS priciest
FROM jobs;
```

<!-- result -->
**Result:**

| total | average | cheapest | priciest |
|---|---|---|---|
| 1580.0 | 105.33 | 0.0 | 360.0 |

*1 row*
<!-- /result -->

**GROUP BY** — how many customers per city:

```sql
SELECT city, COUNT(*) AS customers
FROM customers
GROUP BY city
ORDER BY customers DESC;
```

<!-- result -->
**Result:**

| city | customers |
|---|---|
| Caracas | 4 |
| Valencia | 2 |
| Maracay | 1 |
| Barquisimeto | 1 |

*4 rows*
<!-- /result -->

Jobs by status:

```sql
SELECT status, COUNT(*) AS jobs
FROM jobs
GROUP BY status;
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

Work per mechanic — number of jobs and hours (only assigned jobs):

```sql
SELECT m.name, COUNT(*) AS jobs, SUM(j.labor_hours) AS hours
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
GROUP BY m.name
ORDER BY hours DESC;
```

<!-- result -->
**Result:**

| name | jobs | hours |
|---|---|---|
| Ramon Diaz | 6 | 17.0 |
| Elena Castro | 4 | 7.5 |
| Tomas Herrera | 3 | 5.0 |

*3 rows*
<!-- /result -->

Average car year per make:

```sql
SELECT make, COUNT(*) AS cars, ROUND(AVG(year), 1) AS avg_year
FROM cars
GROUP BY make
ORDER BY cars DESC, make;
```

<!-- result -->
**Result:**

| make | cars | avg_year |
|---|---|---|
| Toyota | 3 | 2017.7 |
| Chevrolet | 2 | 2009.0 |
| Ford | 2 | 2011.5 |
| Hyundai | 1 | 2014.0 |
| Kia | 1 | 2017.0 |
| Mitsubishi | 1 | 2009.0 |

*6 rows*
<!-- /result -->

## The golden rule of GROUP BY

Every column in `SELECT` must be **either** in the `GROUP BY` **or** inside an aggregate function.
`SELECT city, name, COUNT(*) … GROUP BY city` makes no sense: a city has several names — which one should it show? (SQLite picks one at random-ish instead of erroring. PostgreSQL gives an error. Don't rely on it.)

One more tip: in these examples we group by `m.name` to keep them short. In real data two people can share a name, and they'd be merged into one group. The safe version groups by the id too: `GROUP BY m.id, m.name`.

## Practice

1. How many cars does the workshop have?
2. What's the newest car year and the oldest car year?
3. How many cars does each customer have? (Use `customer_id`.)
4. Total parts cost per status.

<details><summary>Answers</summary>

```sql
SELECT COUNT(*) AS cars FROM cars;
```

<!-- result -->
**Result:**

| cars |
|---|
| 10 |

*1 row*
<!-- /result -->

```sql
SELECT MAX(year) AS newest, MIN(year) AS oldest FROM cars;
```

<!-- result -->
**Result:**

| newest | oldest |
|---|---|
| 2020 | 2008 |

*1 row*
<!-- /result -->

```sql
SELECT customer_id, COUNT(*) AS cars FROM cars GROUP BY customer_id;
```

<!-- result -->
**Result:**

| customer_id | cars |
|---|---|
| 1 | 2 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 2 |
| 6 | 1 |
| 7 | 2 |

*7 rows*
<!-- /result -->

```sql
SELECT status, SUM(parts_cost) AS parts_total FROM jobs GROUP BY status;
```

<!-- result -->
**Result:**

| status | parts_total |
|---|---|
| done | 1150.0 |
| in progress | 430.0 |
| open | 0.0 |

*3 rows*
<!-- /result -->

</details>
