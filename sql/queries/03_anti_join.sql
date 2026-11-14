-- Anti-join: products that have never been ordered.
-- NOT EXISTS keeps a product when the subquery finds no matching order.
SELECT p.name
FROM products AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.product_id = p.product_id
)
ORDER BY p.name;
