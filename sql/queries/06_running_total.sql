-- Running total: how much each customer has spent so far, order by order (cancelled orders left out).
-- sum() OVER (... ORDER BY ...) adds up every row from the start of the partition to the current row.
-- The explicit ROWS frame says exactly that; without it, rows with the same date would be added together.
-- Ben's order 109 has a NULL amount: sum() skips it, so his running total stays at 6.00.
SELECT
    customer_id,
    order_id,
    order_date,
    amount,
    sum(amount) OVER (
        PARTITION BY customer_id
        ORDER BY order_date, order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS spent_so_far
FROM orders
WHERE status <> 'cancelled'
ORDER BY customer_id, order_date, order_id;
