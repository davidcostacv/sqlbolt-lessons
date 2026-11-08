# Lesson 6 — Multi-table queries with JOINs

📘 SQLBolt: https://sqlbolt.com/lesson/select_queries_with_joins · [← Prev](05-review-simple-select.md) · [Next →](07-outer-joins.md)

## The idea in plain words

Real data is split into several tables **on purpose**. Instead of writing the customer's name and phone again on every car, the `cars` table just stores `customer_id = 1`, which points to the row with `id = 1` in `customers`.

```
customers                cars
id │ name        ◄────── customer_id │ make  │ model
 1 │ Ana Rivas             1         │ Toyota│ Corolla
                           1         │ Ford  │ Explorer
```

- `customers.id` is the **primary key** (unique id of each customer).
- `cars.customer_id` is a **foreign key** (it points to a customer).

This is called **normalization**: each fact is stored once. If Ana changes her phone, you change it in one place.

A `JOIN` glues the tables back together for a query: *"for each car, find the customer whose id matches."*

`INNER JOIN` (or just `JOIN`) keeps only the rows that **have a match on both sides**.

## Syntax

```sql norun
SELECT columns
FROM table_a
INNER JOIN table_b
    ON table_a.id = table_b.a_id
WHERE …
ORDER BY …;
```

When two tables have a column with the same name (both have `id`!), write `table.column` so SQL knows which one you mean.

## Practical examples

Each car with its owner's name:

```sql
SELECT customers.name, cars.make, cars.model
FROM cars
INNER JOIN customers ON cars.customer_id = customers.id;
```

<!-- result -->
**Result:**

| name | make | model |
|---|---|---|
| Ana Rivas | Toyota | Corolla |
| Ana Rivas | Ford | Explorer |
| Luis Mendoza | Chevrolet | Aveo |
| Carla Ortega | Toyota | Hilux |
| Pedro Salas | Hyundai | Accent |
| Sofia Pineda | Ford | Fiesta |
| Sofia Pineda | Toyota | Fortuner |
| Jorge Luna | Chevrolet | Optra |
| Valeria Campos | Kia | Rio |
| Valeria Campos | Mitsubishi | Lancer |

*10 rows*
<!-- /result -->

Same thing, shorter, with **table aliases** (`c` and `cu`). This is how most people write it:

```sql
SELECT cu.name, c.make, c.model, c.plate
FROM cars AS c
JOIN customers AS cu ON c.customer_id = cu.id
ORDER BY cu.name;
```

<!-- result -->
**Result:**

| name | make | model | plate |
|---|---|---|---|
| Ana Rivas | Toyota | Corolla | AB123CD |
| Ana Rivas | Ford | Explorer | XY987ZT |
| Carla Ortega | Toyota | Hilux | PQ321RS |
| Jorge Luna | Chevrolet | Optra | MN159OP |
| Luis Mendoza | Chevrolet | Aveo | KL456MN |
| Pedro Salas | Hyundai | Accent | GH741JK |
| Sofia Pineda | Ford | Fiesta | TU852VW |
| Sofia Pineda | Toyota | Fortuner | EF963GH |
| Valeria Campos | Kia | Rio | QR357ST |
| Valeria Campos | Mitsubishi | Lancer | UV246WX |

*10 rows*
<!-- /result -->

Chaining joins — every job with the car and who did it:

```sql
SELECT j.id, j.service, c.plate, m.name AS mechanic
FROM jobs AS j
JOIN cars AS c      ON j.car_id = c.id
JOIN mechanics AS m ON j.mechanic_id = m.id
ORDER BY j.id;
```

<!-- result -->
**Result:**

| id | service | plate | mechanic |
|---|---|---|---|
| 1 | Injector cleaning | AB123CD | Ramon Diaz |
| 2 | Brake pads | KL456MN | Tomas Herrera |
| 3 | Injector replacement | PQ321RS | Ramon Diaz |
| 4 | Alternator repair | XY987ZT | Elena Castro |
| 5 | Brake discs | GH741JK | Tomas Herrera |
| 6 | Fuel pump | TU852VW | Ramon Diaz |
| 7 | Battery check | EF963GH | Elena Castro |
| 8 | Injector cleaning | MN159OP | Ramon Diaz |
| 9 | Starter motor | QR357ST | Elena Castro |
| 10 | Brake fluid flush | AB123CD | Tomas Herrera |
| 11 | Injector replacement | UV246WX | Ramon Diaz |
| 12 | Headlight wiring | KL456MN | Elena Castro |
| 15 | Fuel filter | PQ321RS | Ramon Diaz |

*13 rows*
<!-- /result -->

Notice: jobs **13 and 14 disappeared**. They have no mechanic (`mechanic_id` is NULL), so `INNER JOIN` found no match and dropped them. Lesson 7 fixes that.

Joins + filters: all the jobs Ramon (the injection specialist) did on Toyotas:

```sql
SELECT j.service, c.model, j.opened_on
FROM jobs AS j
JOIN cars AS c      ON j.car_id = c.id
JOIN mechanics AS m ON j.mechanic_id = m.id
WHERE m.name = 'Ramon Diaz'
  AND c.make = 'Toyota';
```

<!-- result -->
**Result:**

| service | model | opened_on |
|---|---|---|
| Injector cleaning | Corolla | 2025-01-12 |
| Injector replacement | Hilux | 2025-03-15 |
| Fuel filter | Hilux | 2025-11-05 |

*3 rows*
<!-- /result -->

Four tables at once — which **customer** each mechanic worked for:

```sql
SELECT m.name AS mechanic, cu.name AS customer, j.service
FROM jobs AS j
JOIN mechanics AS m ON j.mechanic_id = m.id
JOIN cars AS c      ON j.car_id = c.id
JOIN customers AS cu ON c.customer_id = cu.id
WHERE j.status = 'done'
ORDER BY m.name, cu.name;
```

<!-- result -->
**Result:**

| mechanic | customer | service |
|---|---|---|
| Elena Castro | Ana Rivas | Alternator repair |
| Elena Castro | Sofia Pineda | Battery check |
| Elena Castro | Valeria Campos | Starter motor |
| Ramon Diaz | Ana Rivas | Injector cleaning |
| Ramon Diaz | Carla Ortega | Injector replacement |
| Ramon Diaz | Jorge Luna | Injector cleaning |
| Ramon Diaz | Sofia Pineda | Fuel pump |
| Tomas Herrera | Ana Rivas | Brake fluid flush |
| Tomas Herrera | Luis Mendoza | Brake pads |
| Tomas Herrera | Pedro Salas | Brake discs |

*10 rows*
<!-- /result -->

## Common mistakes

- **Forgetting `ON`** → every row matches every row (a *cartesian product*): 10 cars × 8 customers = 80 nonsense rows.
- **Joining the wrong columns**: `ON cars.id = customers.id` runs fine but is wrong — car #1 is not owned by customer #1 because of their ids. Always join foreign key → primary key.
- **Ambiguous column**: `SELECT id FROM cars JOIN customers …` → error, both tables have `id`.

## Practice

1. Every job's service next to the car's plate.
2. All cars owned by customers from Valencia (show customer name, make, model).
3. Every job done by Elena Castro, with the car's make and model.

<details><summary>Answers</summary>

```sql
SELECT j.service, c.plate
FROM jobs AS j
JOIN cars AS c ON j.car_id = c.id;
```

<!-- result -->
**Result:**

| service | plate |
|---|---|
| Injector cleaning | AB123CD |
| Brake pads | KL456MN |
| Injector replacement | PQ321RS |
| Alternator repair | XY987ZT |
| Brake discs | GH741JK |
| Fuel pump | TU852VW |
| Battery check | EF963GH |
| Injector cleaning | MN159OP |
| Starter motor | QR357ST |
| Brake fluid flush | AB123CD |
| Injector replacement | UV246WX |
| Headlight wiring | KL456MN |
| Engine scan | EF963GH |
| Oil leak check | GH741JK |
| Fuel filter | PQ321RS |

*15 rows*
<!-- /result -->

```sql
SELECT cu.name, c.make, c.model
FROM cars AS c
JOIN customers AS cu ON c.customer_id = cu.id
WHERE cu.city = 'Valencia';
```

<!-- result -->
**Result:**

| name | make | model |
|---|---|---|
| Luis Mendoza | Chevrolet | Aveo |
| Valeria Campos | Kia | Rio |
| Valeria Campos | Mitsubishi | Lancer |

*3 rows*
<!-- /result -->

```sql
SELECT j.service, c.make, c.model
FROM jobs AS j
JOIN cars AS c      ON j.car_id = c.id
JOIN mechanics AS m ON j.mechanic_id = m.id
WHERE m.name = 'Elena Castro';
```

<!-- result -->
**Result:**

| service | make | model |
|---|---|---|
| Alternator repair | Ford | Explorer |
| Battery check | Toyota | Fortuner |
| Starter motor | Kia | Rio |
| Headlight wiring | Chevrolet | Aveo |

*4 rows*
<!-- /result -->

</details>
