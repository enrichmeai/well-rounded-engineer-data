-- One row per customer, with what they have bought so far.
-- A LEFT JOIN keeps customers who have never ordered (they get 0 orders and 0.00 revenue).
with order_totals as (
    select
        customer_id,
        count(*)                                        as orders_placed,
        min(order_date)                                 as first_order_date,
        sum(case when is_revenue then amount else 0 end) as lifetime_revenue
    from {{ ref('fct_orders') }}
    group by customer_id
)

select
    c.customer_id,
    c.customer_name,
    c.country,
    c.signup_date,
    coalesce(t.orders_placed, 0)       as orders_placed,
    t.first_order_date,
    coalesce(t.lifetime_revenue, 0)    as lifetime_revenue
from {{ ref('stg_customers') }} as c
left join order_totals as t on t.customer_id = c.customer_id
