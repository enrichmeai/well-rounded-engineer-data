-- ROW_NUMBER: each customer's first order.
-- row_number() numbers the rows inside each PARTITION (one partition per customer), in the ORDER BY
-- order. The first order gets 1. Window functions run after WHERE, so to filter on the number we
-- wrap the query in a CTE. (08_dedupe_qualify.sql shows a shorter way: QUALIFY.)
WITH numbered AS (
    SELECT
        customer_id,
        order_id,
        order_date,
        row_number() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS order_number
    FROM orders
)
SELECT customer_id, order_id, order_date
FROM numbered
WHERE order_number = 1
ORDER BY customer_id;
