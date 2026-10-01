EVAL_SET = [
    {
        "id": 1,
        "question": "How many orders are in the database?",
        "gold_sql": "SELECT COUNT(*) FROM orders",
    },
    {
        "id": 2,
        "question": "How many unique customers do we have?",
        "gold_sql": "SELECT COUNT(DISTINCT customer_unique_id) FROM customers",
    },
    {
        "id": 3,
        "question": "How many orders were delivered late?",
        "gold_sql": """
            SELECT COUNT(*)
            FROM orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date > order_estimated_delivery_date
        """,
    },
    {
        "id": 4,
        "question": "What is the average delivery time for delivered orders?",
        "gold_sql": """
            SELECT AVG(order_delivered_customer_date - order_purchase_timestamp)
            FROM orders
            WHERE order_status = 'delivered'
        """,
    },
    {
        "id": 5,
        "question": "List the top 5 products by number of orders.",
        "gold_sql": """
            SELECT product_id, COUNT(*) AS order_count
            FROM order_items
            GROUP BY product_id
            ORDER BY order_count DESC
            LIMIT 5
        """,
    },
    {
        "id": 6,
        "question": "What is the total revenue from delivered orders?",
        "gold_sql": """
            SELECT SUM(payment_value)
            FROM payments
            JOIN orders ON payments.order_id = orders.order_id
            WHERE orders.order_status = 'delivered'
        """,
    },
    {
        "id": 7,
        "question": "How many orders were placed in 2020?",
        "gold_sql": """
            SELECT COUNT(*)
            FROM orders
            WHERE order_purchase_timestamp >= '2020-01-01'
              AND order_purchase_timestamp < '2021-01-01'
        """,
    },
    {
        "id": 8,
        "question": "What is the average number of items per order?",
        "gold_sql": """
            SELECT AVG(item_count)
            FROM (
                SELECT COUNT(*) AS item_count
                FROM order_items
                GROUP BY order_id
            )
        """,
    },
    {
        "id": 9,
        "question": "List the top 5 customers by total spending.",
        "gold_sql": """
            SELECT customer_unique_id, SUM(payment_value) AS total_spent
            FROM payments
            JOIN orders ON payments.order_id = orders.order_id
            GROUP BY customer_unique_id
            ORDER BY total_spent DESC
            LIMIT 5
        """,
    },
    {
        "id": 10,
        "question": "How many orders have been canceled?",
        "gold_sql": """
            SELECT COUNT(*)
            FROM orders
            WHERE order_status = 'canceled'
        """,
    },
    {
        "id": 11,
        "question": "What is the average payment value for delivered orders?",
        "gold_sql": """
            SELECT AVG(payment_value)
            FROM payments
            JOIN orders ON payments.order_id = orders.order_id
            WHERE orders.order_status = 'delivered'
        """,
    },
    {
        "id": 12,
        "question": "List the top 5 products by total revenue.",
        "gold_sql": """
            SELECT product_id, SUM(payment_value) AS total_revenue
            FROM order_items
            JOIN payments ON order_items.order_id = payments.order_id
            JOIN orders ON order_items.order_id = orders.order_id
            WHERE orders.order_status = 'delivered'
            GROUP BY product_id
            ORDER BY total_revenue DESC
            LIMIT 5
        """,
    },
    {
        "id": 13,
        "question": "How many orders were placed by each customer?",
        "gold_sql": """
            SELECT customer_unique_id, COUNT(*) AS order_count
            FROM orders
            GROUP BY customer_unique_id
            ORDER BY order_count DESC
        """,
    },
    {
        "id": 14,
        "question": "What is the average number of days between order purchase and delivery?",
        "gold_sql": """
            SELECT AVG(order_delivered_customer_date - order_purchase_timestamp)
            FROM orders
            WHERE order_status = 'delivered'
        """,
    },
    {
        "id": 15,
        "question": "List the top 5 customers by number of orders.",
        "gold_sql": """
            SELECT customer_unique_id, COUNT(*) AS order_count
            FROM orders
            GROUP BY customer_unique_id
            ORDER BY order_count DESC
            LIMIT 5
        """,
    },
    {
        "id": 16,
        "question": "How many orders have been returned?",
        "gold_sql": """
            SELECT COUNT(*)
            FROM orders
            WHERE order_status = 'returned'
        """,
    },
    {
        "id": 17,
        "question": "What is the total revenue generated from delivered orders?",
        "gold_sql": """
            SELECT SUM(payment_value)
            FROM payments
            JOIN orders ON payments.order_id = orders.order_id
            WHERE orders.order_status = 'delivered'
        """,
    },
    {
        "id": 18,
        "question": "List the top 5 products by number of unique customers.",
        "gold_sql": """
            SELECT product_id, COUNT(DISTINCT customer_unique_id) AS unique_customers
            FROM order_items
            JOIN orders ON order_items.order_id = orders.order_id
            GROUP BY product_id
            ORDER BY unique_customers DESC
            LIMIT 5
        """,
    },
    {
        "id": 19,
        "question": "How many orders were placed in each month of 2020?",
        "gold_sql": """
            SELECT STRFTIME('%Y-%m', order_purchase_timestamp) AS month, COUNT(*) AS order_count
            FROM orders
            WHERE order_purchase_timestamp >= '2020-01-01'
              AND order_purchase_timestamp < '2021-01-01'
            GROUP BY month
            ORDER BY month
        """,
    },
    {
        "id": 20,
        "question": "What is the average payment value for each payment type?",
        "gold_sql": """
            SELECT payment_type, AVG(payment_value) AS avg_payment_value
            FROM payments
            JOIN orders ON payments.order_id = orders.order_id
            WHERE orders.order_status = 'delivered'
            GROUP BY payment_type
        """,
    },
    {
        "id": 21,
        "question": "List the top 5 customers by average order value.",
        "gold_sql": """
            SELECT customer_unique_id, AVG(payment_value) AS avg_order_value
            FROM payments
            JOIN orders ON payments.order_id = orders.order_id
            WHERE orders.order_status = 'delivered'
            GROUP BY customer_unique_id
            ORDER BY avg_order_value DESC
            LIMIT 5
        """,
    }
]