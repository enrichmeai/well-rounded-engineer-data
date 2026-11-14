-- The NULL trap: "customers outside the UK".
-- Dev has no country. For Dev, country <> 'UK' is NULL (unknown), and WHERE keeps only TRUE rows,
-- so Dev silently disappears. This query returns Ben and Ema only. 11_null_comparison_fix.sql fixes it.
SELECT name, country
FROM customers
WHERE country <> 'UK'
ORDER BY name;
