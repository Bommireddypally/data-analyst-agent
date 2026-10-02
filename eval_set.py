EVAL_SET = [
    {"id": 1, "question": "How many orders are in the database?",
     "gold_sql": "SELECT COUNT(*) FROM orders"},
    {"id": 2, "question": "How many unique customers do we have?",
     "gold_sql": "SELECT COUNT(DISTINCT customer_unique_id) FROM customers"},
    {"id": 3, "question": "How many delivered orders arrived after the estimated delivery date?",
     "gold_sql": """SELECT COUNT(*) FROM orders
                    WHERE order_status = 'delivered'
                    AND order_delivered_customer_date > order_estimated_delivery_date"""},
    {"id": 4, "question": "How many orders have been canceled?",
     "gold_sql": "SELECT COUNT(*) FROM orders WHERE order_status = 'canceled'"},
    {"id": 5, "question": "What is the average review score?",
     "gold_sql": "SELECT AVG(review_score) FROM order_reviews"},
    {"id": 6, "question": "What is the total revenue from delivered orders?",
     "gold_sql": """SELECT SUM(oi.price + oi.freight_value)
                    FROM order_items oi
                    JOIN orders o ON oi.order_id = o.order_id
                    WHERE o.order_status = 'delivered'"""},
    {"id": 7, "question": "How many orders were placed in 2020?",
     "gold_sql": """SELECT COUNT(*) FROM orders
                    WHERE order_purchase_timestamp >= '2020-01-01'
                    AND order_purchase_timestamp < '2021-01-01'"""},
    {"id": 8, "question": "How many orders have been returned?",
     "gold_sql": None},   # no return data exists: read the answer yourself
]