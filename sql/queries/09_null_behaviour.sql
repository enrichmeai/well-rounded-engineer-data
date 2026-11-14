-- How NULL behaves. NULL means "unknown", and SQL follows that idea everywhere.
-- Order 109 has a NULL amount; the other nine orders add up to 152.00.
SELECT
    count(*)                     AS all_rows,          -- 10: counts rows
    count(amount)                AS rows_with_amount,  -- 9: counts non-NULL values
    sum(amount)                  AS total,             -- 152.00: NULL is skipped
    round(avg(amount), 2)        AS avg_known,         -- 16.89: 152.00 / 9, NULL is skipped
    round(avg(coalesce(amount, 0)), 2) AS avg_null_as_zero, -- 15.20: 152.00 / 10
    (NULL = NULL)                AS null_equals_null,  -- NULL, not true: unknown = unknown is unknown
    (NULL IS NOT DISTINCT FROM NULL) AS null_not_distinct, -- true: compares NULLs as equal
    (3 NOT IN (1, 2, NULL))      AS not_in_with_null   -- NULL: 3 might equal the unknown value
FROM orders;
