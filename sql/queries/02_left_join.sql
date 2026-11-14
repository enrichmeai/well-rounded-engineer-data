-- LEFT JOIN: every customer, with how many orders they placed.
-- A left join keeps every row from the left table, even when nothing on the right matches.
-- Ema has no orders, so her order columns are NULL. count(o.order_id) counts only non-NULL values,
-- so she gets 0. count(*) would count her row and give 1: try it.
SELECT
    c.name,
    count(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.name
ORDER BY order_count DESC, c.name;
