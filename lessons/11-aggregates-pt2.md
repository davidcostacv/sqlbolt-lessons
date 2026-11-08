# Lesson 11 — Queries with aggregates (Part 2): HAVING

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_with_aggregates_pt_2 · [← Prev](10-aggregates-pt1.md) · [Next →](12-order-of-execution.md)

## The idea in plain words

`WHERE` filters **rows before** they get grouped.
`HAVING` filters **groups after** they're calculated.

Example question: *"Which customers have **more than one** car?"*
You can't write `WHERE COUNT(*) > 1` — at the moment `WHERE` runs, nothing has been counted yet. So you count first (`GROUP BY`), then filter the groups (`HAVING`).

| | Filters | Can use aggregates like `COUNT()`? |
|---|---|---|
| `WHERE` | individual rows, before grouping | ❌ no |
| `HAVING` | groups, after grouping | ✅ yes |

## Syntax

```sql norun
SELECT group_column, AGG_FUNC(column)
FROM table
WHERE row_condition
GROUP BY group_column
HAVING group_condition;
```

## Practical examples

Customers with more than one car:

```sql
SELECT cu.name, COUNT(*) AS cars
FROM cars AS c
JOIN customers AS cu ON c.customer_id = cu.id
GROUP BY cu.name
HAVING COUNT(*) > 1;
```

<!-- result -->
**Result:**

| name | cars |
|---|---|
| Ana Rivas | 2 |
| Sofia Pineda | 2 |
| Valeria Campos | 2 |

*3 rows*
<!-- /result -->

Mechanics who have billed more than $500 in parts:

```sql
SELECT m.name, SUM(j.parts_cost) AS parts_total
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
GROUP BY m.name
HAVING SUM(j.parts_cost) > 500
ORDER BY parts_total DESC;
```

<!-- result -->
**Result:**

| name | parts_total |
|---|---|
| Ramon Diaz | 1005.0 |

*1 row*
<!-- /result -->

`WHERE` **and** `HAVING` together — only **finished** jobs (WHERE, per row), then only mechanics with at least 3 of them (HAVING, per group):

```sql
SELECT m.name, COUNT(*) AS finished_jobs
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
WHERE j.status = 'done'
GROUP BY m.name
HAVING COUNT(*) >= 3;
```

<!-- result -->
**Result:**

| name | finished_jobs |
|---|---|
| Elena Castro | 3 |
| Ramon Diaz | 4 |
| Tomas Herrera | 3 |

*3 rows*
<!-- /result -->

Services we have done more than once (our "popular" services):

```sql
SELECT service, COUNT(*) AS times
FROM jobs
GROUP BY service
HAVING times > 1
ORDER BY times DESC, service;
```

<!-- result -->
**Result:**

| service | times |
|---|---|
| Injector cleaning | 2 |
| Injector replacement | 2 |

*2 rows*
<!-- /result -->

(SQLite lets you use the alias `times` in `HAVING`. Some databases don't — repeating `COUNT(*)` always works.)

Cities where customers have more than 2 cars in total:

```sql
SELECT cu.city, COUNT(c.id) AS cars
FROM customers AS cu
JOIN cars AS c ON c.customer_id = cu.id
GROUP BY cu.city
HAVING COUNT(c.id) > 2;
```

<!-- result -->
**Result:**

| city | cars |
|---|---|
| Caracas | 5 |
| Valencia | 3 |

*2 rows*
<!-- /result -->

## Common mistakes

- **`WHERE COUNT(*) > 1`** → error "misuse of aggregate". Use `HAVING`.
- **Putting row filters in `HAVING`** (`HAVING status = 'done'`). PostgreSQL rejects it with an error; SQLite runs it but gives **wrong counts without warning** (it checks the status of just one row per group). Row filters always go in `WHERE`.

## Practice

1. Car makes that appear 2 or more times in the workshop.
2. Cars (by plate) that came in for more than one job.
3. Among **done** jobs only, which mechanics averaged more than 2 labor hours per job?

<details><summary>Answers</summary>

```sql
SELECT make, COUNT(*) AS cars FROM cars GROUP BY make HAVING COUNT(*) >= 2;
```

<!-- result -->
**Result:**

| make | cars |
|---|---|
| Chevrolet | 2 |
| Ford | 2 |
| Toyota | 3 |

*3 rows*
<!-- /result -->

```sql
SELECT c.plate, COUNT(*) AS jobs
FROM jobs AS j
JOIN cars AS c ON j.car_id = c.id
GROUP BY c.plate
HAVING COUNT(*) > 1;
```

<!-- result -->
**Result:**

| plate | jobs |
|---|---|
| AB123CD | 2 |
| EF963GH | 2 |
| GH741JK | 2 |
| KL456MN | 2 |
| PQ321RS | 2 |

*5 rows*
<!-- /result -->

```sql
SELECT m.name, ROUND(AVG(j.labor_hours), 2) AS avg_hours
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
WHERE j.status = 'done'
GROUP BY m.name
HAVING AVG(j.labor_hours) > 2;
```

<!-- result -->
**Result:**

| name | avg_hours |
|---|---|
| Ramon Diaz | 2.88 |

*1 row*
<!-- /result -->

</details>
