# Lesson 9 — Queries with expressions

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_with_expressions · [← Prev](08-nulls.md) · [Next →](10-aggregates-pt1.md)

## The idea in plain words

You're not limited to columns as they are stored. You can **calculate** new values on the fly, like formulas in Excel:

- math: `+ - * /` and `%` (remainder)
- text: `||` glues text together (`'Ana' || ' ' || 'Rivas'`)
- functions: `ROUND()`, `UPPER()`, `LENGTH()`, `SUBSTR()`, `ABS()`…

Give every calculated column a name with `AS`, otherwise the column title is the whole formula.

Expressions work in `SELECT`, `WHERE` and `ORDER BY`.

## Syntax

```sql norun
SELECT expression AS name
FROM table
WHERE expression > something
ORDER BY expression;
```

## Practical examples

How much is each job's labor worth? `labor_hours × mechanic's hourly rate`:

```sql
SELECT j.id, j.service, j.labor_hours, m.hourly_rate,
       j.labor_hours * m.hourly_rate AS labor_usd
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
ORDER BY j.id
LIMIT 5;
```

<!-- result -->
**Result:**

| id | service | labor_hours | hourly_rate | labor_usd |
|---|---|---|---|---|
| 1 | Injector cleaning | 2.0 | 18.0 | 36.0 |
| 2 | Brake pads | 1.5 | 15.0 | 22.5 |
| 3 | Injector replacement | 4.0 | 18.0 | 72.0 |
| 4 | Alternator repair | 3.0 | 20.0 | 60.0 |
| 5 | Brake discs | 2.5 | 15.0 | 37.5 |

*5 rows*
<!-- /result -->

The total invoice per job = labor + parts:

```sql
SELECT j.id, j.service,
       j.labor_hours * m.hourly_rate + j.parts_cost AS total_usd
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
ORDER BY total_usd DESC
LIMIT 5;
```

<!-- result -->
**Result:**

| id | service | total_usd |
|---|---|---|
| 11 | Injector replacement | 441.0 |
| 3 | Injector replacement | 392.0 |
| 6 | Fuel pump | 273.0 |
| 9 | Starter motor | 230.0 |
| 4 | Alternator repair | 210.0 |

*5 rows*
<!-- /result -->

Use an expression in `WHERE`: jobs whose invoice is over $300:

```sql
SELECT j.id, j.service
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
WHERE j.labor_hours * m.hourly_rate + j.parts_cost > 300;
```

<!-- result -->
**Result:**

| id | service |
|---|---|
| 3 | Injector replacement |
| 11 | Injector replacement |

*2 rows*
<!-- /result -->

How old is each car? (taking 2025 as "this year"):

```sql
SELECT make, model, year, 2025 - year AS age_years
FROM cars
ORDER BY age_years DESC;
```

<!-- result -->
**Result:**

| make | model | year | age_years |
|---|---|---|---|
| Chevrolet | Optra | 2008 | 17 |
| Mitsubishi | Lancer | 2009 | 16 |
| Chevrolet | Aveo | 2010 | 15 |
| Ford | Fiesta | 2011 | 14 |
| Ford | Explorer | 2012 | 13 |
| Hyundai | Accent | 2014 | 11 |
| Toyota | Corolla | 2015 | 10 |
| Kia | Rio | 2017 | 8 |
| Toyota | Hilux | 2018 | 7 |
| Toyota | Fortuner | 2020 | 5 |

*10 rows*
<!-- /result -->

Text expressions — a label for the dashboard:

```sql
SELECT make || ' ' || model || ' (' || year || ')' AS car,
       UPPER(plate) AS plate
FROM cars
LIMIT 4;
```

<!-- result -->
**Result:**

| car | plate |
|---|---|
| Toyota Corolla (2015) | AB123CD |
| Ford Explorer (2012) | XY987ZT |
| Chevrolet Aveo (2010) | KL456MN |
| Toyota Hilux (2018) | PQ321RS |

*4 rows*
<!-- /result -->

Prices with 16% tax, rounded to 2 decimals:

```sql
SELECT service, parts_cost, ROUND(parts_cost * 1.16, 2) AS with_tax
FROM jobs
WHERE parts_cost > 100;
```

<!-- result -->
**Result:**

| service | parts_cost | with_tax |
|---|---|---|
| Injector replacement | 320.0 | 371.2 |
| Alternator repair | 150.0 | 174.0 |
| Brake discs | 140.0 | 162.4 |
| Fuel pump | 210.0 | 243.6 |
| Starter motor | 180.0 | 208.8 |
| Injector replacement | 360.0 | 417.6 |

*6 rows*
<!-- /result -->

## ⚠️ The integer division trap

In SQLite, `integer / integer` drops the decimals:

```sql
SELECT 7 / 2 AS integer_division, 7 / 2.0 AS real_division;
```

<!-- result -->
**Result:**

| integer_division | real_division |
|---|---|
| 3 | 3.5 |

*1 row*
<!-- /result -->

If you need decimals, make one side a decimal number (`2.0`) or multiply by `1.0` first.

## Practice

1. Show each mechanic's rate for an 8-hour day.
2. Show each car as `"PLATE - Make Model"` in one column called `label`.
3. Cars made in an even year (hint: `year % 2 = 0`).

<details><summary>Answers</summary>

```sql
SELECT name, hourly_rate * 8 AS day_rate FROM mechanics;
```

<!-- result -->
**Result:**

| name | day_rate |
|---|---|
| Ramon Diaz | 144.0 |
| Elena Castro | 160.0 |
| Tomas Herrera | 120.0 |
| Lucia Morales | 176.0 |

*4 rows*
<!-- /result -->

```sql
SELECT plate || ' - ' || make || ' ' || model AS label FROM cars;
```

<!-- result -->
**Result:**

| label |
|---|
| AB123CD - Toyota Corolla |
| XY987ZT - Ford Explorer |
| KL456MN - Chevrolet Aveo |
| PQ321RS - Toyota Hilux |
| GH741JK - Hyundai Accent |
| TU852VW - Ford Fiesta |
| EF963GH - Toyota Fortuner |
| MN159OP - Chevrolet Optra |
| QR357ST - Kia Rio |
| UV246WX - Mitsubishi Lancer |

*10 rows*
<!-- /result -->

```sql
SELECT make, model, year FROM cars WHERE year % 2 = 0;
```

<!-- result -->
**Result:**

| make | model | year |
|---|---|---|
| Ford | Explorer | 2012 |
| Chevrolet | Aveo | 2010 |
| Toyota | Hilux | 2018 |
| Hyundai | Accent | 2014 |
| Toyota | Fortuner | 2020 |
| Chevrolet | Optra | 2008 |

*6 rows*
<!-- /result -->

</details>
