How it Works

Though it looks like just data cleaning, this project was actually a full ETL and analytics pipeline that scaled from 1.1M+ raw Amazon rows down to a structured dataset of 268K unique products, stored in a normalized database and visualized in an interactive dashboard.

Setting up data (Extract)

I ingested 141 CSV files (1,134,172 rows) using Python (pandas, os). Logging original row counts and cleaning results ensured visibility into data quality at scale.

Cleaning & normalization (Transform)

Deduplication → Removed 571K+ duplicates through a two-pass strategy (per-file + global), cutting redundancy by almost 50%.

Null handling → Dropped 263K+ rows missing product names/ratings (~23% of the data).

Data type standardization → Cleaned 1M+ rating and price fields with regex + numeric coercion; excluded absurd outliers over $100K.

Final result → 268K unique products, 11 standardized columns, representing a 75% reduction from raw input.

Loading & modeling (Load)

I built a SQLite database with:

products → 268K unique rows, each with a generated product_id

amazon_data → 1.1M cleaned rows, preserving category metadata

This schema eliminated redundancy and optimized joins.

Query layer & analysis

Across the cleaned dataset, I ran analyses such as:

High-rated products with <10 reviews (signal: early gems)

Average prices across dozens of categories

95th / 10th percentile thresholds → ~26K premium products and ~26K budget products

Most-reviewed products → top 20 items with tens of thousands of reviews

Biggest discounts → markdowns of 90%+ off

I exported a 500K-row dataset for dashboards with discount %, categories, and subcategories.

Dashboard

I built an Excel dashboard with PivotTables & PivotCharts over the 500K export, visualizing discounts, prices, ratings, and category segmentation. This allowed interactive exploration across hundreds of thousands of products.

Challenges

Working with over 1 million rows across 140+ CSVs wasn’t straightforward. Here are the biggest challenges I faced and solved:

Hidden duplicates – Products repeated across categories looked unique until I ran a two-pass deduplication strategy. This removed 571K redundant rows and cut dataset size nearly in half.

Mixed numeric fields – Ratings and prices often came in with symbols, commas, or text. I cleaned 1M+ entries using regex and coercion, while filtering out absurd outliers.

Critical nulls – Over 263K rows were missing essential fields (name, ratings). I dropped them early to protect downstream joins and aggregates.

Cross-file inconsistencies – Ingesting 141 CSVs meant inconsistent file naming and access errors. I solved this with os.path validation, exception handling, and logging.

Scalability for BI – Excel dashboards can lag on large datasets. By exporting a curated 500K-row dataset, I balanced scale with performance, enabling smooth PivotTable interactivity.

Link to dashboard: 
https://1drv.ms/x/c/d78d5fc6af87fc76/IQSoNrWPAj6sR6JG56F4nOBGAfupBEaYvYWDdPsarJk8Isc?em=2&wdHideGridlines=True&wdHideHeaders=True&wdDownloadButton=True&wdInConfigurator=True&wdInConfigurator=True
