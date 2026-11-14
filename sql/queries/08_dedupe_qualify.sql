-- Deduplication with QUALIFY: keep only the latest email for each customer.
-- customer_emails_raw has exact duplicates (Ben, Chloe) and older emails (Asha, Chloe).
-- QUALIFY filters on a window function, the way HAVING filters on an aggregate, so no CTE is needed.
-- Ben's two rows are identical, so it does not matter which of them row_number() calls 1.
-- If two DIFFERENT rows tied on loaded_at, add a column to the ORDER BY to make the choice deterministic.
SELECT customer_id, email, loaded_at
FROM customer_emails_raw
QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY loaded_at DESC) = 1
ORDER BY customer_id;
