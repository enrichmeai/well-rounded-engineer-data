-- INNER JOIN: every order, with the customer's name and the product's name.
-- An inner join keeps a row only when both sides match. Every order has a customer and a product,
-- so all 10 orders come back. Ema has no orders, so she does not appear at all.
SELECT
    o.order_id,
    c.name AS customer,
    p.name AS product,
    o.amount
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN products  AS p ON p.product_id  = o.product_id
ORDER BY o.order_id;
