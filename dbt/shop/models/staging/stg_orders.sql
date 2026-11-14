select
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    amount,                         -- NULL until the order is priced
    lower(trim(status)) as status
from {{ ref('raw_orders') }}
