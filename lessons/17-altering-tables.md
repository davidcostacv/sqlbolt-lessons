# Lesson 17 — Altering tables

📘 SQLBolt: https://sqlbolt.com/lesson/altering_tables · [← Prev](16-creating-tables.md) · [Next →](18-dropping-tables.md)

## The idea in plain words

Needs change. Months later the boss says *"we need each customer's email"*. You don't delete the table and start over — you **alter** it.

`ALTER TABLE` can:
- **add** a column
- **remove** a column
- **rename** a column
- **rename** the table

## Syntax

```sql norun
ALTER TABLE table ADD COLUMN column TYPE CONSTRAINTS DEFAULT value;
ALTER TABLE table DROP COLUMN column;
ALTER TABLE table RENAME COLUMN old_name TO new_name;
ALTER TABLE table RENAME TO new_table_name;
```

## Practical examples

Add an `email` column to customers. Existing rows get NULL (we don't know their emails yet):

```sql
ALTER TABLE customers ADD COLUMN email TEXT;
```

<!-- result -->
**Result:**

✔ ALTER OK
<!-- /result -->

```sql
SELECT id, name, email FROM customers LIMIT 3;
```

<!-- result -->
**Result:**

| id | name | email |
|---|---|---|
| 1 | Ana Rivas | NULL |
| 2 | Luis Mendoza | NULL |
| 3 | Carla Ortega | NULL |

*3 rows*
<!-- /result -->

Add a column **with a default** — every existing car gets `'gasoline'` automatically:

```sql
ALTER TABLE cars ADD COLUMN fuel TEXT NOT NULL DEFAULT 'gasoline';
```

<!-- result -->
**Result:**

✔ ALTER OK
<!-- /result -->

```sql
SELECT plate, model, fuel FROM cars LIMIT 3;
```

<!-- result -->
**Result:**

| plate | model | fuel |
|---|---|---|
| AB123CD | Corolla | gasoline |
| XY987ZT | Explorer | gasoline |
| KL456MN | Aveo | gasoline |

*3 rows*
<!-- /result -->

> Adding a `NOT NULL` column **without** a default fails when the table has rows: what value would the old rows get?

```sql error
ALTER TABLE cars ADD COLUMN vin TEXT NOT NULL;
```

<!-- result -->
**Result:**

❌ Error: `Cannot add a NOT NULL column with default value NULL`
<!-- /result -->

Fill the new column for one customer:

```sql
UPDATE customers SET email = 'ana.rivas@example.com' WHERE id = 1;
```

<!-- result -->
**Result:**

✔ UPDATE OK — 1 row affected
<!-- /result -->

Rename a column to something clearer:

```sql
ALTER TABLE jobs RENAME COLUMN parts_cost TO parts_usd;
```

<!-- result -->
**Result:**

✔ ALTER OK
<!-- /result -->

```sql
SELECT id, service, parts_usd FROM jobs LIMIT 3;
```

<!-- result -->
**Result:**

| id | service | parts_usd |
|---|---|---|
| 1 | Injector cleaning | 35.0 |
| 2 | Brake pads | 60.0 |
| 3 | Injector replacement | 320.0 |

*3 rows*
<!-- /result -->

Remove a column we don't need anymore:

```sql
ALTER TABLE customers DROP COLUMN email;
```

<!-- result -->
**Result:**

✔ ALTER OK
<!-- /result -->

Rename a whole table:

```sql
ALTER TABLE mechanics RENAME TO staff;
```

<!-- result -->
**Result:**

✔ ALTER OK
<!-- /result -->

```sql
SELECT name, specialty FROM staff;
```

<!-- result -->
**Result:**

| name | specialty |
|---|---|
| Ramon Diaz | Fuel injection |
| Elena Castro | Electrical |
| Tomas Herrera | Brakes |
| Lucia Morales | Diagnostics |

*4 rows*
<!-- /result -->

## Careful in real projects

- Dropping a column **deletes that data** forever.
- Renaming breaks every query and app that uses the old name. In real apps, schema changes go through **migrations**: small numbered SQL files (`001_add_email.sql`, `002_…`) saved in git, so every copy of the database changes the same way. Tools like Prisma, Supabase or Alembic manage them for you.
- SQLite's `ALTER TABLE` is limited (e.g., you can't change a column's type). For those, the trick is: create a new table, copy the data, drop the old, rename the new.

## Practice

1. Add an `is_vip` column to customers, default `0`.
2. Make Ana and Sofia VIP.
3. Show the VIP customers.

<details><summary>Answers</summary>

```sql
ALTER TABLE customers ADD COLUMN is_vip BOOLEAN NOT NULL DEFAULT 0;
```

<!-- result -->
**Result:**

✔ ALTER OK
<!-- /result -->

```sql
UPDATE customers SET is_vip = 1 WHERE name IN ('Ana Rivas', 'Sofia Pineda');
```

<!-- result -->
**Result:**

✔ UPDATE OK — 2 rows affected
<!-- /result -->

```sql
SELECT name, is_vip FROM customers WHERE is_vip = 1;
```

<!-- result -->
**Result:**

| name | is_vip |
|---|---|
| Ana Rivas | 1 |
| Sofia Pineda | 1 |

*2 rows*
<!-- /result -->

</details>
