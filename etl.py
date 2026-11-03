import pandas as pd
import logging

# Set up logging to track pipeline progress and errors
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def extract():
    logging.info("Extracting data...")
    try:
        orders = pd.read_csv('data/raw/olist_orders_dataset.csv')
        customers = pd.read_csv('data/raw/olist_customers_dataset.csv')
        return orders, customers
    except FileNotFoundError as e:
        logging.error(f"File not found. Check your paths: {e}")
        raise

def transform(orders_df, customers_df):
    logging.info("Transforming data...")
    try:
        # Drop nulls and fix dates
        orders_df = orders_df.dropna()
        orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
        orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
        
        # Feature Engineering: Order month and Delivery days
        orders_df['order_month'] = orders_df['order_purchase_timestamp'].dt.strftime('%Y-%m')
        orders_df['delivery_days'] = (orders_df['order_delivered_customer_date'] - orders_df['order_purchase_timestamp']).dt.days
        
        # Text Standardization: Lowercase and strip extra spaces
        customers_df['customer_city'] = customers_df['customer_city'].str.lower().str.strip()
        
        # Deduplicate and join
        orders_df = orders_df.drop_duplicates()
        customers_df = customers_df.drop_duplicates()
        merged_df = pd.merge(orders_df, customers_df, on='customer_id', how='inner')
        
        return merged_df
    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        raise

def load(df):
    logging.info("Loading data to Parquet...")
    try:
        df.to_parquet('data/clean/cleaned_olist_data.parquet', index=False)
        logging.info("Pipeline complete!")
    except Exception as e:
        logging.error(f"Failed to save Parquet file: {e}")
        raise

if __name__ == "__main__":
    raw_orders, raw_customers = extract()
    clean_data = transform(raw_orders, raw_customers)
    load(clean_data)