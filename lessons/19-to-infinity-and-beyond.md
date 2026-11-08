# Lesson X — To infinity and beyond

📘 SQLBolt: https://sqlbolt.com/lesson/end · [← Prev](18-dropping-tables.md) · [Back to index](../README.md)

You finished the basics 🎉. Here's a taste of what comes next, all runnable on the same workshop data.

## 1. Subqueries — a query inside a query

*"Jobs that cost more in parts than the average job"*. First you'd need the average, then the filter. A subquery does both:

```sql
SELECT id, service, parts_cost
FROM jobs
WHERE parts_cost > (SELECT AVG(parts_cost) FROM jobs)
ORDER BY parts_cost DESC;
```

<!-- result -->
**Result:**

| id | service | parts_cost |
|---|---|---|
| 11 | Injector replacement | 360.0 |
| 3 | Injector replacement | 320.0 |
| 6 | Fuel pump | 210.0 |
| 9 | Starter motor | 180.0 |
| 4 | Alternator repair | 150.0 |
| 5 | Brake discs | 140.0 |

*6 rows*
<!-- /result -->

The inner `( … )` runs first and becomes a single number.

`IN` with a subquery — customers who have at least one Toyota:

```sql
SELECT name FROM customers
WHERE id IN (SELECT customer_id FROM cars WHERE make = 'Toyota');
```

<!-- result -->
**Result:**

| name |
|---|
| Ana Rivas |
| Carla Ortega |
| Sofia Pineda |

*3 rows*
<!-- /result -->

## 2. CASE — if/else inside SQL

Label each job by size:

```sql
SELECT id, service, parts_cost,
       CASE
           WHEN parts_cost >= 200 THEN 'big'
           WHEN parts_cost >= 50  THEN 'medium'
           ELSE 'small'
       END AS size
FROM jobs
ORDER BY parts_cost DESC
LIMIT 6;
```

<!-- result -->
**Result:**

| id | service | parts_cost | size |
|---|---|---|---|
| 11 | Injector replacement | 360.0 | big |
| 3 | Injector replacement | 320.0 | big |
| 6 | Fuel pump | 210.0 | big |
| 9 | Starter motor | 180.0 | medium |
| 4 | Alternator repair | 150.0 | medium |
| 5 | Brake discs | 140.0 | medium |

*6 rows*
<!-- /result -->

## 3. Common Table Expressions (WITH) — name a step

When a query gets long, split it into named steps with `WITH`, like variables. Step 1 calculates the invoice of every **finished** job; step 2 adds them up per customer:

```sql
WITH invoice AS (
    SELECT j.id, c.customer_id,
           j.labor_hours * m.hourly_rate + j.parts_cost AS total
    FROM jobs AS j
    JOIN cars AS c      ON j.car_id = c.id
    JOIN mechanics AS m ON j.mechanic_id = m.id
    WHERE j.status = 'done'
)
SELECT cu.name, COUNT(*) AS paid_jobs, SUM(i.total) AS spent_usd
FROM invoice AS i
JOIN customers AS cu ON cu.id = i.customer_id
GROUP BY cu.id, cu.name
ORDER BY spent_usd DESC;
```

<!-- result -->
**Result:**

| name | paid_jobs | spent_usd |
|---|---|---|
| Carla Ortega | 1 | 392.0 |
| Ana Rivas | 3 | 316.0 |
| Sofia Pineda | 2 | 283.0 |
| Valeria Campos | 1 | 230.0 |
| Pedro Salas | 1 | 177.5 |
| Luis Mendoza | 1 | 82.5 |
| Jorge Luna | 1 | 71.0 |

*7 rows*
<!-- /result -->

*"Who are our best customers (by finished, billed work)?"* — answered. (We group by `cu.id` too, so two customers with the same name would never be mixed together.)

## 4. UNION — stack two results

All the people the workshop deals with, in one list. `UNION ALL` keeps every row; plain `UNION` also removes duplicate rows (slower, and only needed if duplicates can appear):

```sql
SELECT name, 'customer' AS role FROM customers
UNION ALL
SELECT name, 'mechanic' FROM mechanics
ORDER BY role, name;
```

<!-- result -->
**Result:**

| name | role |
|---|---|
| Ana Rivas | customer |
| Carla Ortega | customer |
| Jorge Luna | customer |
| Luis Mendoza | customer |
| Miguel Torres | customer |
| Pedro Salas | customer |
| Sofia Pineda | customer |
| Valeria Campos | customer |
| Elena Castro | mechanic |
| Lucia Morales | mechanic |
| Ramon Diaz | mechanic |
| Tomas Herrera | mechanic |

*12 rows*
<!-- /result -->

## 5. Window functions — rank without grouping away the rows

Rank each mechanic's jobs by price, keeping every row:

```sql
SELECT m.name, j.service, j.parts_cost,
       RANK() OVER (PARTITION BY m.name ORDER BY j.parts_cost DESC) AS rank_in_mechanic
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
WHERE m.name IN ('Elena Castro', 'Tomas Herrera');
```

<!-- result -->
**Result:**

| name | service | parts_cost | rank_in_mechanic |
|---|---|---|---|
| Elena Castro | Starter motor | 180.0 | 1 |
| Elena Castro | Alternator repair | 150.0 | 2 |
| Elena Castro | Headlight wiring | 25.0 | 3 |
| Elena Castro | Battery check | 0.0 | 4 |
| Tomas Herrera | Brake discs | 140.0 | 1 |
| Tomas Herrera | Brake pads | 60.0 | 2 |
| Tomas Herrera | Brake fluid flush | 20.0 | 3 |

*7 rows*
<!-- /result -->

## 6. Indexes — make lookups fast

An index is like the index at the back of a book: the database finds rows without reading the whole table. You add them on columns you filter or join by a lot:

```sql
CREATE INDEX idx_jobs_car_id ON jobs(car_id);
```

<!-- result -->
**Result:**

✔ CREATE OK
<!-- /result -->

On 15 rows you won't notice. On 15 million you will.

## Where to go from here

- **SQLite docs** (the engine used in this repo): https://www.sqlite.org/lang.html
- **PostgreSQL tutorial** (what Supabase uses): https://www.postgresql.org/docs/current/tutorial.html
- **Practice more**: https://sqlzoo.net and https://www.sql-practice.com
- **Use it for real**: point `tools/run.py`'s idea at your own data — export a CSV from a spreadsheet, load it into SQLite (`sqlite3 my.db` → `.import --csv file.csv table`), and ask it questions.
