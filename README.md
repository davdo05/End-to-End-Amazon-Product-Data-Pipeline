# How it Works

At first glance this might look like simple cleaning, but it’s actually a full **ETL and analytics pipeline** that scaled from **1.1 million raw Amazon product rows** down to a structured dataset of just **268,000 unique, analysis-ready entries**.

---

## Setting up data (Extract)

I ingested **141 CSV files** containing **1,134,172 raw product rows** using Python (`pandas`, `os`). Each file represented a different Amazon product category or subcategory. By programmatically iterating through the directory, I logged record counts and cleaning results to keep track of quality at scale.

---

## Cleaning & normalization (Transform)

**Deduplication**: I removed a total of **571,000+ duplicate rows**, achieved through **two passes** — one within each file and a second global pass across the merged dataset. Many duplicates came from products listed under multiple categories. Without this, almost **50% of the dataset** would have been redundant.

**Null handling**: Out of the initial dataset, I dropped **263,000+ rows** with missing `name` or `ratings`, which represented about **23% of the raw data**. This ensured that only reliable, complete records entered downstream analysis.

**Data type standardization**: I converted all rating fields to numeric, eliminating several thousand string artifacts, and cleaned **1M+ price fields** by stripping symbols/commas and coercing to floats, filtering outliers beyond **$100K**.

After transformation, I consolidated the data into **268,000 unique product entries across 11 standardized columns**, representing a **75% reduction** from the raw size.

---

## Loading & modeling (Load)

I built a **SQLite database** with:

- **products** → **268,000 rows**, one per unique product, with generated `product_id`.  
- **amazon_data** → **1.1M+ rows**, the cleaned but denormalized full dataset, preserving category links.  

This structure allowed me to compute aggregates quickly without duplicating fields.

---

## Query layer & analysis

With SQL, I ran analyses across **hundreds of thousands of rows** efficiently:

- **High-rated, low-review items** → surfaced **20 products** with ≥4.5 ratings but fewer than 10 reviews.  
- **Average price by category** → computed means across **dozens of product categories**, showing which categories had the highest and lowest average prices.  
- **Percentile analysis** → calculated 95th and 10th percentile thresholds across all **268K unique prices**, isolating ~**26,000 premium items** and ~**26,000 budget items**.  
- **Most-reviewed products** → ranked top **20 items**, each with **tens of thousands of reviews**, showing popularity at scale.  
- **Top discounts** → identified items with up to **90%+ off**, computed using SQL discount formulas.  

I then exported a **500K-row curated dataset** with discount %, categories, and product IDs, optimized for dashboards.

---

## Dashboard

In Excel, I used **PivotTables and PivotCharts** over the **500K exported records** to visualize:

- category-level price distributions,  
- rating vs. review count scatter patterns,  
- discount distributions,  
- and segmentation across product categories.  

This dashboard let me interactively explore trends across **hundreds of thousands of products**, not just a sample.

---

## What ETL means here

- **Extract** → Consolidated **141 raw CSVs (1.1M+ rows)** into pandas.  
- **Transform** → Removed **571K+ duplicates**, dropped **263K nulls**, enforced numeric formats across **1M+ fields**, standardized **11 columns**.  
- **Load** → Stored results into a **268K-row normalized products table** plus a **1.1M-row amazon_data table**, and exported a **500K-row BI dataset**.  

---

## Challenges I ran into (and how I solved them)

- **Hidden duplicates at scale** → Solved by designing a **two-pass deduplication strategy**, which cut out **571K redundant rows**.  
- **Mixed numeric fields** → Cleaned **1M+ entries** in price and ratings columns using regex and float coercion.  
- **Critical nulls** → Dropped **263K+ rows** missing essential fields, preserving dataset integrity.  
- **Cross-file inconsistencies** → Used `os.path` validation and error handling to process **140+ file paths** reliably.  
- **Scalability for BI** → Exported a **500K-row dashboard dataset**, ensuring smooth PivotTable interaction despite data size.  


Link to dashboard: 
https://1drv.ms/x/c/d78d5fc6af87fc76/IQSoNrWPAj6sR6JG56F4nOBGAfupBEaYvYWDdPsarJk8Isc?em=2&wdHideGridlines=True&wdHideHeaders=True&wdDownloadButton=True&wdInConfigurator=True&wdInConfigurator=True
