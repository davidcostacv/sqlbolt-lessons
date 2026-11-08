# Lesson 1 — SELECT queries 101

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_introduction · [Next →](02-constraints-pt1.md)

## The idea in plain words

A database is a bunch of **tables**. A table is like an Excel sheet:

- each **column** is one kind of information (name, city, phone…)
- each **row** is one thing (one customer, one car…)

`SELECT` is how you **ask** the database for data. It never changes anything — it only reads.
Think of it as: *"Show me these columns, from that table."*

## Syntax

```sql norun
SELECT column1, column2
FROM table_name;
```

- `SELECT` → which columns you want, separated by commas
- `FROM` → which table they live in
- `*` → shortcut for "all the columns"
- The `;` marks the end of the query

SQL keywords are not case-sensitive (`select` = `SELECT`), but writing them in CAPITALS makes queries easier to read.

## Practical examples (workshop database)

Our practice database is a small car repair workshop. Let's see the customers table — all columns:

```sql
SELECT * FROM customers;
```

<!-- result -->
**Result:**

| id | name | city | phone | joined_on |
|---|---|---|---|---|
| 1 | Ana Rivas | Caracas | 0414-555-0101 | 2023-02-14 |
| 2 | Luis Mendoza | Valencia | 0424-555-0102 | 2023-06-03 |
| 3 | Carla Ortega | Caracas | NULL | 2023-09-21 |
| 4 | Pedro Salas | Maracay | 0412-555-0104 | 2024-01-10 |
| 5 | Sofia Pineda | Caracas | 0416-555-0105 | 2024-03-30 |
| 6 | Jorge Luna | Barquisimeto | NULL | 2024-07-18 |
| 7 | Valeria Campos | Valencia | 0414-555-0107 | 2025-01-05 |
| 8 | Miguel Torres | Caracas | 0426-555-0108 | 2025-04-22 |

*8 rows*
<!-- /result -->

Usually you don't need everything. Only the name and the city:

```sql
SELECT name, city FROM customers;
```

<!-- result -->
**Result:**

| name | city |
|---|---|
| Ana Rivas | Caracas |
| Luis Mendoza | Valencia |
| Carla Ortega | Caracas |
| Pedro Salas | Maracay |
| Sofia Pineda | Caracas |
| Jorge Luna | Barquisimeto |
| Valeria Campos | Valencia |
| Miguel Torres | Caracas |

*8 rows*
<!-- /result -->

The order you write the columns is the order you get them back:

```sql
SELECT plate, make, model FROM cars;
```

<!-- result -->
**Result:**

| plate | make | model |
|---|---|---|
| AB123CD | Toyota | Corolla |
| XY987ZT | Ford | Explorer |
| KL456MN | Chevrolet | Aveo |
| PQ321RS | Toyota | Hilux |
| GH741JK | Hyundai | Accent |
| TU852VW | Ford | Fiesta |
| EF963GH | Toyota | Fortuner |
| MN159OP | Chevrolet | Optra |
| QR357ST | Kia | Rio |
| UV246WX | Mitsubishi | Lancer |

*10 rows*
<!-- /result -->

You can also give a column a nicer name in the result with `AS` (an *alias*):

```sql
SELECT name AS mechanic, hourly_rate AS usd_per_hour
FROM mechanics;
```

<!-- result -->
**Result:**

| mechanic | usd_per_hour |
|---|---|
| Ramon Diaz | 18.0 |
| Elena Castro | 20.0 |
| Tomas Herrera | 15.0 |
| Lucia Morales | 22.0 |

*4 rows*
<!-- /result -->

## Common mistakes

- **Forgetting the comma** between columns: `SELECT name city` doesn't give two columns — SQL reads it as "the column `name`, renamed to `city`". Sneaky!
- **Misspelling a column**: `SELECT nmae FROM customers` → error "no such column".
- **Using `*` everywhere**: fine for exploring, but in real apps pick only the columns you need — it's faster and clearer.

## Practice

Try them with `python tools/run.py` before opening the answer.

1. Show the `service` of every job.
2. Show the `make`, `model` and `year` of every car.
3. Show every column of the `mechanics` table.

<details><summary>Answers</summary>

```sql
SELECT service FROM jobs;
```

<!-- result -->
**Result:**

| service |
|---|
| Injector cleaning |
| Brake pads |
| Injector replacement |
| Alternator repair |
| Brake discs |
| Fuel pump |
| Battery check |
| Injector cleaning |
| Starter motor |
| Brake fluid flush |
| Injector replacement |
| Headlight wiring |
| Engine scan |
| Oil leak check |
| Fuel filter |

*15 rows*
<!-- /result -->

```sql
SELECT make, model, year FROM cars;
```

<!-- result -->
**Result:**

| make | model | year |
|---|---|---|
| Toyota | Corolla | 2015 |
| Ford | Explorer | 2012 |
| Chevrolet | Aveo | 2010 |
| Toyota | Hilux | 2018 |
| Hyundai | Accent | 2014 |
| Ford | Fiesta | 2011 |
| Toyota | Fortuner | 2020 |
| Chevrolet | Optra | 2008 |
| Kia | Rio | 2017 |
| Mitsubishi | Lancer | 2009 |

*10 rows*
<!-- /result -->

```sql
SELECT * FROM mechanics;
```

<!-- result -->
**Result:**

| id | name | specialty | hourly_rate | hired_on |
|---|---|---|---|---|
| 1 | Ramon Diaz | Fuel injection | 18.0 | 2019-05-01 |
| 2 | Elena Castro | Electrical | 20.0 | 2020-08-15 |
| 3 | Tomas Herrera | Brakes | 15.0 | 2022-02-01 |
| 4 | Lucia Morales | Diagnostics | 22.0 | 2025-09-01 |

*4 rows*
<!-- /result -->

</details>
