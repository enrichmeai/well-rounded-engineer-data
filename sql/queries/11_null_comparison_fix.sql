-- The fix: IS DISTINCT FROM treats NULL as a value of its own, so NULL is distinct from 'UK'.
-- Now Dev is included. (WHERE country <> 'UK' OR country IS NULL says the same thing, longer.)
SELECT name, country
FROM customers
WHERE country IS DISTINCT FROM 'UK'
ORDER BY name;
