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
     "gold_sql": None},   
         {"id": 9, "question": "Which customer state has the most orders? Return the state and the order count.",
     "gold_sql": """SELECT c.customer_state, COUNT(*) FROM orders o
                    JOIN customers c ON o.customer_id = c.customer_id
                    GROUP BY c.customer_state ORDER BY 2 DESC LIMIT 1"""},
    {"id": 10, "question": "List the top 5 customer states by number of orders. Return the state and the order count.",
     "gold_sql": """SELECT c.customer_state, COUNT(*) FROM orders o
                    JOIN customers c ON o.customer_id = c.customer_id
                    GROUP BY c.customer_state ORDER BY 2 DESC LIMIT 5"""},
    {"id": 11, "question": "What is the average payment value for each payment type? Return the type and the average.",
     "gold_sql": "SELECT payment_type, AVG(payment_value) FROM order_payments GROUP BY payment_type"},
    {"id": 12, "question": "What percentage of delivered orders arrived after the estimated date, rounded to 2 decimals?",
     "gold_sql": """SELECT ROUND(100.0 * SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date
                    THEN 1 ELSE 0 END) / COUNT(*), 2) FROM orders WHERE order_status = 'delivered'"""},
    {"id": 13, "question": "How many distinct products were sold?",
     "gold_sql": "SELECT COUNT(DISTINCT product_id) FROM order_items"},
    {"id": 14, "question": "How many reviews have a score of 1?",
     "gold_sql": "SELECT COUNT(*) FROM order_reviews WHERE review_score = 1"},
    {"id": 15, "question": "What is the average review score for each customer state? Return the state and the average.",
     "gold_sql": """SELECT c.customer_state, AVG(r.review_score) FROM order_reviews r
                    JOIN orders o ON r.order_id = o.order_id
                    JOIN customers c ON o.customer_id = c.customer_id
                    GROUP BY c.customer_state"""},
    {"id": 16, "question": "What is the average age of our customers?",
     "gold_sql": None},   # trap: no age data exists, read the answer
]