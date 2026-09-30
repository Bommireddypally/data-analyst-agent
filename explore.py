import duckdb

con = duckdb.connect("olist.duckdb", read_only=True)

# print(con.execute("SHOW TABLES").fetchall())
# print(con.execute("""
#     SELECT order_status, COUNT(*) AS n
#     FROM orders
#     GROUP BY order_status
#     ORDER BY n DESC
# """).fetchdf())

print(con.execute("""DESCRIBE orders;""").fetchdf())
print(con.execute("""DESCRIBE customers;""").fetchdf())