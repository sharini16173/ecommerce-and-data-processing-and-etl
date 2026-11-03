# Olist E-Commerce ETL Pipeline

## Project Overview
This project is an automated Python ETL (Extract, Transform, Load) pipeline that processes raw e-commerce transaction data. It cleans missing values, standardizes datetime formats, joins multiple tables, and exports a highly compressed Parquet file ready for dashboard visualization.

## Data Pipeline Steps
1. **Extract:** Loads raw `orders` and `customers` CSV files using Pandas.
2. **Transform:** 
   - Drops incomplete orders missing delivery dates.
   - Converts text-based timestamps to functional Datetime objects.
   - Generates a new `order_month` feature for time-series analysis.
   - Deduplicates records and performs an inner join on `customer_id`.
3. **Load:** Exports the cleaned, merged dataset as a columnar Parquet file to reduce storage footprint and optimize read speeds.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Execute the pipeline: `python etl.py`