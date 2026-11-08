# Lesson 4 — Filtering and sorting query results

📘 SQLBolt: https://sqlbolt.com/lesson/filtering_sorting_query_results · [← Prev](03-constraints-pt2.md) · [Next →](05-review-simple-select.md)

## The idea in plain words

Three new tools to control **what comes back** and **in what order**:

- `DISTINCT` → remove repeated rows. *"Which cities do we have customers in?"* (each city once)
- `ORDER BY` → sort. `ASC` = small→big / A→Z (the default), `DESC` = big→small / Z→A
- `LIMIT` and `OFFSET` → only give me N rows, optionally skipping the first M. Perfect for "top 3" lists or pagination (page 1, page 2…).

Without `ORDER BY`, the database **does not promise any order**. If order matters, always say it.

## Syntax

```sql norun
SELECT DISTINCT column
FROM table
WHERE condition
ORDER BY column ASC/DESC
LIMIT how_many OFFSET how_many_to_skip;
```

## Practical examples

Which cities do our customers come from? (each city once)

```sql
SELECT DISTINCT city FROM customers ORDER BY city;
```

<!-- result -->
**Result:**

| city |
|---|
| Barquisimeto |
| Caracas |
| Maracay |
| Valencia |

*4 rows*
<!-- /result -->

Cars from newest to oldest:

```sql
SELECT make, model, year FROM cars ORDER BY year DESC;
```

<!-- result -->
**Result:**

| make | model | year |
|---|---|---|
| Toyota | Fortuner | 2020 |
| Toyota | Hilux | 2018 |
| Kia | Rio | 2017 |
| Toyota | Corolla | 2015 |
| Hyundai | Accent | 2014 |
| Ford | Explorer | 2012 |
| Ford | Fiesta | 2011 |
| Chevrolet | Aveo | 2010 |
| Mitsubishi | Lancer | 2009 |
| Chevrolet | Optra | 2008 |

*10 rows*
<!-- /result -->

Sort by two columns — first by make A→Z, and inside the same make, newest first:

```sql
SELECT make, model, year FROM cars ORDER BY make ASC, year DESC;
```

<!-- result -->
**Result:**

| make | model | year |
|---|---|---|
| Chevrolet | Aveo | 2010 |
| Chevrolet | Optra | 2008 |
| Ford | Explorer | 2012 |
| Ford | Fiesta | 2011 |
| Hyundai | Accent | 2014 |
| Kia | Rio | 2017 |
| Mitsubishi | Lancer | 2009 |
| Toyota | Fortuner | 2020 |
| Toyota | Hilux | 2018 |
| Toyota | Corolla | 2015 |

*10 rows*
<!-- /result -->

The top 3 most expensive jobs in parts:

```sql
SELECT service, parts_cost FROM jobs ORDER BY parts_cost DESC LIMIT 3;
```

<!-- result -->
**Result:**

| service | parts_cost |
|---|---|
| Injector replacement | 360.0 |
| Injector replacement | 320.0 |
| Fuel pump | 210.0 |

*3 rows*
<!-- /result -->

Pagination: show customers 3 at a time. Page 2 = skip the first 3, take the next 3:

```sql
SELECT id, name FROM customers ORDER BY id LIMIT 3 OFFSET 3;
```

<!-- result -->
**Result:**

| id | name |
|---|---|
| 4 | Pedro Salas |
| 5 | Sofia Pineda |
| 6 | Jorge Luna |

*3 rows*
<!-- /result -->

## How to think about "page N"

`OFFSET = (page - 1) × page_size`. Page 1 → `OFFSET 0`, page 2 → `OFFSET 3`, page 3 → `OFFSET 6`.

## Common mistakes

- **`LIMIT` without `ORDER BY`** → "the first 3" is random-ish. Always sort first.
- **`DISTINCT` works on the whole row**, not one column. `SELECT DISTINCT make, model` removes rows where *both* make and model repeat.
- **Order of clauses matters**: `ORDER BY` goes after `WHERE`, and `LIMIT` goes last.

## Practice

1. List every distinct `service` in the jobs table, A→Z.
2. The 2 newest customers (by `joined_on`).
3. The 3 cheapest mechanics by hourly rate.
4. Jobs list ordered by id, page 3 when showing 5 per page.

<details><summary>Answers</summary>

```sql
SELECT DISTINCT service FROM jobs ORDER BY service;
```

<!-- result -->
**Result:**

| service |
|---|
| Alternator repair |
| Battery check |
| Brake discs |
| Brake fluid flush |
| Brake pads |
| Engine scan |
| Fuel filter |
| Fuel pump |
| Headlight wiring |
| Injector cleaning |
| Injector replacement |
| Oil leak check |
| Starter motor |

*13 rows*
<!-- /result -->

```sql
SELECT name, joined_on FROM customers ORDER BY joined_on DESC LIMIT 2;
```

<!-- result -->
**Result:**

| name | joined_on |
|---|---|
| Miguel Torres | 2025-04-22 |
| Valeria Campos | 2025-01-05 |

*2 rows*
<!-- /result -->

```sql
SELECT name, hourly_rate FROM mechanics ORDER BY hourly_rate ASC LIMIT 3;
```

<!-- result -->
**Result:**

| name | hourly_rate |
|---|---|
| Tomas Herrera | 15.0 |
| Ramon Diaz | 18.0 |
| Elena Castro | 20.0 |

*3 rows*
<!-- /result -->

```sql
SELECT id, service FROM jobs ORDER BY id LIMIT 5 OFFSET 10;
```

<!-- result -->
**Result:**

| id | service |
|---|---|
| 11 | Injector replacement |
| 12 | Headlight wiring |
| 13 | Engine scan |
| 14 | Oil leak check |
| 15 | Fuel filter |

*5 rows*
<!-- /result -->

</details>
