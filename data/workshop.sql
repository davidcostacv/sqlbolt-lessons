-- Practice database for every lesson: a small, made-up car repair workshop.
-- All names, plates and phone numbers are fictional.
--
--   customers 1───* cars 1───* jobs *───1 mechanics
--
-- Loaded fresh (in memory) every time you run tools/run.py, so you can't break anything.

CREATE TABLE customers (
    id        INTEGER PRIMARY KEY,
    name      TEXT    NOT NULL,
    city      TEXT    NOT NULL,
    phone     TEXT,              -- can be NULL (we don't have everyone's phone)
    joined_on TEXT    NOT NULL   -- dates are stored as 'YYYY-MM-DD' text in SQLite
);

CREATE TABLE cars (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    make        TEXT    NOT NULL,
    model       TEXT    NOT NULL,
    year        INTEGER NOT NULL,
    plate       TEXT    NOT NULL UNIQUE
);

CREATE TABLE mechanics (
    id          INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    specialty   TEXT    NOT NULL,
    hourly_rate REAL    NOT NULL,  -- USD per hour of labor
    hired_on    TEXT    NOT NULL
);

CREATE TABLE jobs (
    id          INTEGER PRIMARY KEY,
    car_id      INTEGER NOT NULL REFERENCES cars(id),
    mechanic_id INTEGER REFERENCES mechanics(id),  -- NULL = nobody assigned yet
    service     TEXT    NOT NULL,
    labor_hours REAL    NOT NULL,
    parts_cost  REAL    NOT NULL,                   -- USD
    opened_on   TEXT    NOT NULL,
    status      TEXT    NOT NULL                    -- 'open', 'in progress' or 'done'
);

INSERT INTO customers (id, name, city, phone, joined_on) VALUES
    (1, 'Ana Rivas',      'Caracas',      '0414-555-0101', '2023-02-14'),
    (2, 'Luis Mendoza',   'Valencia',     '0424-555-0102', '2023-06-03'),
    (3, 'Carla Ortega',   'Caracas',      NULL,            '2023-09-21'),
    (4, 'Pedro Salas',    'Maracay',      '0412-555-0104', '2024-01-10'),
    (5, 'Sofia Pineda',   'Caracas',      '0416-555-0105', '2024-03-30'),
    (6, 'Jorge Luna',     'Barquisimeto', NULL,            '2024-07-18'),
    (7, 'Valeria Campos', 'Valencia',     '0414-555-0107', '2025-01-05'),
    (8, 'Miguel Torres',  'Caracas',      '0426-555-0108', '2025-04-22');
-- Miguel (8) has no cars registered yet → useful for LEFT JOIN lessons.

INSERT INTO cars (id, customer_id, make, model, year, plate) VALUES
    (1,  1, 'Toyota',    'Corolla',  2015, 'AB123CD'),
    (2,  1, 'Ford',      'Explorer', 2012, 'XY987ZT'),
    (3,  2, 'Chevrolet', 'Aveo',     2010, 'KL456MN'),
    (4,  3, 'Toyota',    'Hilux',    2018, 'PQ321RS'),
    (5,  4, 'Hyundai',   'Accent',   2014, 'GH741JK'),
    (6,  5, 'Ford',      'Fiesta',   2011, 'TU852VW'),
    (7,  5, 'Toyota',    'Fortuner', 2020, 'EF963GH'),
    (8,  6, 'Chevrolet', 'Optra',    2008, 'MN159OP'),
    (9,  7, 'Kia',       'Rio',      2017, 'QR357ST'),
    (10, 7, 'Mitsubishi','Lancer',   2009, 'UV246WX');

INSERT INTO mechanics (id, name, specialty, hourly_rate, hired_on) VALUES
    (1, 'Ramon Diaz',     'Fuel injection', 18.0, '2019-05-01'),
    (2, 'Elena Castro',   'Electrical',     20.0, '2020-08-15'),
    (3, 'Tomas Herrera',  'Brakes',         15.0, '2022-02-01'),
    (4, 'Lucia Morales',  'Diagnostics',    22.0, '2025-09-01');
-- Lucia (4) was just hired and has no jobs yet.

INSERT INTO jobs (id, car_id, mechanic_id, service, labor_hours, parts_cost, opened_on, status) VALUES
    (1,  1,  1,    'Injector cleaning',     2.0,  35.0, '2025-01-12', 'done'),
    (2,  3,  3,    'Brake pads',            1.5,  60.0, '2025-02-03', 'done'),
    (3,  4,  1,    'Injector replacement',  4.0, 320.0, '2025-03-15', 'done'),
    (4,  2,  2,    'Alternator repair',     3.0, 150.0, '2025-04-02', 'done'),
    (5,  5,  3,    'Brake discs',           2.5, 140.0, '2025-05-20', 'done'),
    (6,  6,  1,    'Fuel pump',             3.5, 210.0, '2025-06-11', 'done'),
    (7,  7,  2,    'Battery check',         0.5,   0.0, '2025-07-01', 'done'),
    (8,  8,  1,    'Injector cleaning',     2.0,  35.0, '2025-08-09', 'done'),
    (9,  9,  2,    'Starter motor',         2.5, 180.0, '2025-09-14', 'done'),
    (10, 1,  3,    'Brake fluid flush',     1.0,  20.0, '2025-10-02', 'done'),
    (11, 10, 1,    'Injector replacement',  4.5, 360.0, '2025-10-25', 'in progress'),
    (12, 3,  2,    'Headlight wiring',      1.5,  25.0, '2025-11-01', 'in progress'),
    (13, 7,  NULL, 'Engine scan',           1.0,   0.0, '2025-11-03', 'open'),
    (14, 5,  NULL, 'Oil leak check',        1.0,   0.0, '2025-11-04', 'open'),
    (15, 4,  1,    'Fuel filter',           1.0,  45.0, '2025-11-05', 'in progress');
-- Jobs 13 and 14 have no mechanic (NULL) → useful for NULL and OUTER JOIN lessons.
