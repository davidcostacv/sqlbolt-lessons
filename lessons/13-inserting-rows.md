# Lesson 13 — Inserting rows

📘 SQLBolt: https://sqlbolt.com/lesson/inserting_rows · [← Prev](12-order-of-execution.md) · [Next →](14-updating-rows.md)

## The idea in plain words

Until now we only **read**. Now we **write**. `INSERT` adds new rows to a table — a new customer walks in, a new car, a new job.

A table has a **schema**: the fixed list of columns, their types, and their rules (`NOT NULL`, `UNIQUE`…). Every row you insert must follow it, or the database refuses.

> 🧪 In this repo every lesson starts from a fresh copy of the data, so the examples below build on each other **within this lesson** only. Experiment freely with `python tools/run.py`.

## Syntax

```sql norun
-- recommended: name the columns
INSERT INTO table (column1, column2)
VALUES (value1, value2);

-- several rows at once
INSERT INTO table (column1, column2)
VALUES (value1, value2),
       (value3, value4);
```

You *can* skip the column list (`INSERT INTO table VALUES (…)`) but then you must give a value for **every** column in the exact order. If someone adds a column later, your query breaks. Always name the columns.

## Practical examples

A new customer walks in. We don't give the `id`: an `INTEGER PRIMARY KEY` fills itself with the next number.

```sql
INSERT INTO customers (name, city, phone, joined_on)
VALUES ('Daniela Rojas', 'Maracay', '0414-555-0109', '2025-11-06');
```

<!-- result -->
**Result:**

✔ INSERT OK — 1 row affected
<!-- /result -->

Check it — she got id 9 automatically:

```sql
SELECT * FROM customers WHERE name = 'Daniela Rojas';
```

<!-- result -->
**Result:**

| id | name | city | phone | joined_on |
|---|---|---|---|---|
| 9 | Daniela Rojas | Maracay | 0414-555-0109 | 2025-11-06 |

*1 row*
<!-- /result -->

She brought two cars. Insert both at once:

```sql
INSERT INTO cars (customer_id, make, model, year, plate)
VALUES (9, 'Toyota', 'Yaris', 2016, 'ZZ111AA'),
       (9, 'Renault', 'Logan', 2013, 'ZZ222BB');
```

<!-- result -->
**Result:**

✔ INSERT OK — 2 rows affected
<!-- /result -->

And a job for the Yaris (car 11). No mechanic yet → we just leave `mechanic_id` out and it stays NULL:

```sql
INSERT INTO jobs (car_id, service, labor_hours, parts_cost, opened_on, status)
VALUES (11, 'Injector cleaning', 2.0, 35.0, '2025-11-06', 'open');
```

<!-- result -->
**Result:**

✔ INSERT OK — 1 row affected
<!-- /result -->

You can use expressions while inserting:

```sql
INSERT INTO mechanics (name, specialty, hourly_rate, hired_on)
VALUES ('Andres Pena', 'Suspension', 15.0 * 1.10, DATE('2025-11-06'));
```

<!-- result -->
**Result:**

✔ INSERT OK — 1 row affected
<!-- /result -->

```sql
SELECT name, hourly_rate, hired_on FROM mechanics WHERE name = 'Andres Pena';
```

<!-- result -->
**Result:**

| name | hourly_rate | hired_on |
|---|---|---|
| Andres Pena | 16.5 | 2025-11-06 |

*1 row*
<!-- /result -->

## When the database says no

The schema protects you. A car with a plate that already exists breaks the `UNIQUE` rule:

```sql error
INSERT INTO cars (customer_id, make, model, year, plate)
VALUES (1, 'Kia', 'Picanto', 2019, 'AB123CD');
```

<!-- result -->
**Result:**

❌ Error: `UNIQUE constraint failed: cars.plate`
<!-- /result -->

A customer without a name breaks `NOT NULL`:

```sql error
INSERT INTO customers (city, joined_on) VALUES ('Caracas', '2025-11-06');
```

<!-- result -->
**Result:**

❌ Error: `NOT NULL constraint failed: customers.name`
<!-- /result -->

A car for customer 999, who doesn't exist, breaks the **foreign key**:

```sql error
INSERT INTO cars (customer_id, make, model, year, plate)
VALUES (999, 'Kia', 'Picanto', 2019, 'NEW0001');
```

<!-- result -->
**Result:**

❌ Error: `FOREIGN KEY constraint failed`
<!-- /result -->

These errors are **good**: they stop bad data from getting in.

> ⚠️ Two SQLite quirks to know:
> - **Foreign keys are OFF by default in SQLite.** You must run `PRAGMA foreign_keys = ON;` on every connection (this repo's tools do it for you). PostgreSQL and MySQL always enforce them.
> - **SQLite doesn't enforce column types.** Putting `'abc'` into an `INTEGER` column is accepted. The constraints (`NOT NULL`, `UNIQUE`, `CHECK`, foreign keys) *are* enforced. If you need strict types, create the table with `STRICT` (Lesson 16).

## Practice

1. Add a new customer from Valencia with no phone.
2. Add a "Brake pads" job for car 3 assigned to mechanic 3, 1.5 hours, $60 parts, opened today, status `'open'`.
3. Check how many jobs exist now.

<details><summary>Answers</summary>

```sql
INSERT INTO customers (name, city, joined_on)
VALUES ('Gabriel Mora', 'Valencia', '2025-11-07');
```

<!-- result -->
**Result:**

✔ INSERT OK — 1 row affected
<!-- /result -->

```sql
INSERT INTO jobs (car_id, mechanic_id, service, labor_hours, parts_cost, opened_on, status)
VALUES (3, 3, 'Brake pads', 1.5, 60.0, '2025-11-07', 'open');
```

<!-- result -->
**Result:**

✔ INSERT OK — 1 row affected
<!-- /result -->

```sql
SELECT COUNT(*) AS jobs FROM jobs;
```

<!-- result -->
**Result:**

| jobs |
|---|
| 17 |

*1 row*
<!-- /result -->

(15 original + 1 from the examples + 1 from the practice = 17.)

</details>
