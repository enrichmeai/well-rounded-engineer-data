-- One row per order, with the product's category and a flag saying whether it counts as revenue.
-- The rule lives in one place: an order counts when it is not cancelled and has an amount.
select
    o.order_id,
    o.customer_id,
    o.product_id,
    p.category,
    o.order_date,
    o.quantity,
    o.amount,
    o.status,
    (o.status <> 'cancelled' and o.amount is not null) as is_revenue
from {{ ref('stg_orders') }} as o
join {{ ref('stg_products') }} as p on p.product_id = o.product_id
