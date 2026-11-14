-- Staging: one model per source table. Rename, cast and clean here, and nothing else.
select
    customer_id,
    name as customer_name,
    country,                        -- may be NULL: Dev did not give one
    signup_date
from {{ ref('raw_customers') }}
