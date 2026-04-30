import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/sales.db")

# ── Query 1: Total revenue and profit ──
q1 = pd.read_sql("""
    SELECT 
        ROUND(SUM(sales), 2)  AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit,
        COUNT(*)              AS total_orders
    FROM orders
""", engine)
print("=== OVERALL BUSINESS ===")
print(q1)

# ── Query 2: Sales by region ──
q2 = pd.read_sql("""
    SELECT 
        region,
        ROUND(SUM(sales), 2)  AS revenue,
        ROUND(SUM(profit), 2) AS profit
    FROM orders
    GROUP BY region
    ORDER BY revenue DESC
""", engine)
print("\n=== SALES BY REGION ===")
print(q2)

# ── Query 3: Sales by category ──
q3 = pd.read_sql("""
    SELECT 
        category,
        ROUND(SUM(sales), 2)        AS revenue,
        ROUND(SUM(profit), 2)       AS profit,
        ROUND(AVG(discount)*100, 1) AS avg_discount_pct
    FROM orders
    GROUP BY category
    ORDER BY revenue DESC
""", engine)
print("\n=== SALES BY CATEGORY ===")
print(q3)

# ── Query 4: Monthly revenue trend ──
q4 = pd.read_sql("""
    SELECT 
        STRFTIME('%Y-%m', order_date) AS month,
        ROUND(SUM(sales), 2)          AS revenue
    FROM orders
    GROUP BY month
    ORDER BY month
""", engine)
print("\n=== MONTHLY TREND ===")
print(q4)

# ── Query 5: Top 5 most profitable products ──
q5 = pd.read_sql("""
    SELECT 
        product_name,
        ROUND(SUM(profit), 2) AS total_profit
    FROM orders
    GROUP BY product_name
    ORDER BY total_profit DESC
    LIMIT 5
""", engine)
print("\n=== TOP 5 PRODUCTS ===")
print(q5)