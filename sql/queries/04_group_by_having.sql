-- GROUP BY with HAVING: customers who have spent at least 30.00, cancelled orders left out.
-- WHERE filters rows BEFORE they are grouped (here: drop cancelled orders).
-- HAVING filters groups AFTER they are aggregated (here: keep customers whose total is >= 30).
-- Ben's order 109 has no amount yet (NULL); sum() skips NULLs, so his total is 6.00.
SELECT
    c.name,
    count(*)      AS orders,
    sum(o.amount) AS revenue
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.status <> 'cancelled'
GROUP BY c.name
HAVING sum(o.amount) >= 30
ORDER BY revenue DESC;
