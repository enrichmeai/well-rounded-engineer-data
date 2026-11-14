-- LAG: how many days passed since the same customer's previous order.
-- lag(order_date) reads order_date from the previous row in the partition. A customer's first order
-- has no previous row, so lag() returns NULL, and so does the date difference.
SELECT
    customer_id,
    order_id,
    order_date,
    lag(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS previous_order_date,
    date_diff(
        'day',
        lag(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id),
        order_date
    ) AS days_since_previous
FROM orders
ORDER BY customer_id, order_date, order_id;
