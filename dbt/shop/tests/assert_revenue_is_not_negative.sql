-- A singular data test: any row this query returns is a failure.
select order_id, amount
from {{ ref('fct_orders') }}
where amount < 0
