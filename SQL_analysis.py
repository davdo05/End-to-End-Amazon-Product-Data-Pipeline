import pandas as pd
import sqlite3
import re

# Step 1: Load the cleaned data
df = pd.read_csv("combined_amazon_data.csv")

# Step 2: Clean price columns
def clean_price(price_str):
    if isinstance(price_str, str):
        # Remove commas,  symbols, whitespace
        clean = re.sub(r'[^\d.]', '', price_str)
        try:
            value = float(clean)
            # Filter out absurd values for better analysis 
            return value if 1 <= value <= 100000 else None
        except:
            return None
    return price_str

df['actual_price'] = df['actual_price'].apply(clean_price)
df['discount_price'] = df['discount_price'].apply(clean_price)

# Step 3: Create products table
products = df[['name', 'ratings', 'no_of_ratings', 'discount_price', 'actual_price']].drop_duplicates().copy()
products['product_id'] = products.reset_index().index + 1

# Step 4: Merge product_id into full dataset
df = df.merge(products, on=['name', 'ratings', 'no_of_ratings', 'discount_price', 'actual_price'], how='left')

# Step 5: Store into SQLite
conn = sqlite3.connect("amazon_products.db")
products.to_sql("products", conn, if_exists="replace", index=False)
df.to_sql("amazon_data", conn, if_exists="replace", index=False)
print(" Tables created: 'products' and 'amazon_data'")

# Step 6: Run SQL queries
query = """
SELECT name, ratings, CAST(no_of_ratings AS INTEGER) AS no_of_ratings,
       discount_price, actual_price
FROM amazon_data
WHERE CAST(no_of_ratings AS INTEGER) < 10 AND CAST(ratings AS FLOAT) >= 4.5
ORDER BY ratings ASC
LIMIT 20;

"""
result = pd.read_sql_query(query, conn)
print("\n High-rated, low-review products:\n", result)

query = """
SELECT a.main_category, AVG(p.actual_price) AS avg_price
FROM products p
JOIN amazon_data a ON p.name = a.name
GROUP BY a.main_category
ORDER BY avg_price DESC;
"""
result = pd.read_sql_query(query, conn)
print("\n💡 Average actual price by category:\n", result)


# Step 1: Calculate 90th percentile threshold in Python
high_price_threshold = products['actual_price'].quantile(0.95)

# Step 2: Query
query = f"""
SELECT name, actual_price, ratings, no_of_ratings
FROM products
WHERE actual_price >= {high_price_threshold}
ORDER BY actual_price DESC
LIMIT 20; 
"""
result = pd.read_sql_query(query, conn)
print("\n High-priced products and their ratings:\n", result)

low_price_threshold = products['actual_price'].quantile(0.1)

query = f"""
SELECT name, actual_price, ratings, no_of_ratings
FROM products
WHERE actual_price <= {low_price_threshold}
ORDER BY actual_price ASC
LIMIT 20; 
"""
result = pd.read_sql_query(query, conn)
print("\n🧾 Low-priced products and their ratings:\n", result)


query = """
SELECT name, CAST(no_of_ratings AS INTEGER) AS no_of_ratings, ratings, discount_price, actual_price
FROM products
ORDER BY CAST(no_of_ratings AS INTEGER) DESC
LIMIT 20;
"""
result = pd.read_sql_query(query, conn)
print("\n Most-reviewed products:\n", result)

query = """
SELECT name, discount_price, actual_price, ratings, no_of_ratings,
       ROUND((actual_price - discount_price) * 100.0 / actual_price, 2) AS discount_percent
FROM products
WHERE discount_price < actual_price
ORDER BY discount_percent DESC
LIMIT 20;
"""
result = pd.read_sql_query(query, conn)
print("\n Top discounted products and their ratings:\n", result)

# Save full dataset from SQL to Excel
query = """ 
SELECT DISTINCT
    p.product_id,
    p.name,
    p.ratings,
    CAST(p.no_of_ratings AS INTEGER) AS no_of_ratings,
    p.discount_price,
    p.actual_price,
    ROUND((p.actual_price - p.discount_price) * 100.0 / p.actual_price, 2) AS discount_percent,
    a.main_category,
    a.sub_category
FROM products p
JOIN amazon_data a ON p.name = a.name
WHERE p.actual_price IS NOT NULL AND p.discount_price IS NOT NULL
"""
df_dashboard = pd.read_sql_query(query, conn)
#df_dashboard.head(500_000).to_excel("amazon_dashboard_sample.xlsx", index=False)