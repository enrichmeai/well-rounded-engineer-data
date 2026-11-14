-- Creates the four shop tables and loads them from the CSV files in data/.
-- Run from inside the sql/ folder, because the paths below are relative to it.
-- Explicit column types make the schema part of the lesson, instead of leaving it to type detection.

CREATE OR REPLACE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        VARCHAR NOT NULL,
    country     VARCHAR,              -- Dev has no country: an empty field in the CSV becomes NULL
    signup_date DATE    NOT NULL
);

CREATE OR REPLACE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       VARCHAR       NOT NULL,
    category   VARCHAR       NOT NULL,
    price      DECIMAL(10, 2) NOT NULL
);

CREATE OR REPLACE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    order_date  DATE    NOT NULL,
    quantity    INTEGER NOT NULL,
    amount      DECIMAL(10, 2),       -- order 109 has not been priced yet, so its amount is NULL
    status      VARCHAR NOT NULL
);

-- A raw copy of an email feed, as it might arrive from another system: it has exact duplicates
-- and older versions of the same customer's email.
CREATE OR REPLACE TABLE customer_emails_raw (
    customer_id INTEGER   NOT NULL,
    email       VARCHAR   NOT NULL,
    loaded_at   TIMESTAMP NOT NULL
);

COPY customers           FROM 'data/customers.csv'           (HEADER);
COPY products            FROM 'data/products.csv'            (HEADER);
COPY orders              FROM 'data/orders.csv'              (HEADER);
COPY customer_emails_raw FROM 'data/customer_emails_raw.csv' (HEADER);
