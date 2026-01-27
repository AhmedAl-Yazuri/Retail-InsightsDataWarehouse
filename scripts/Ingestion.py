from sqlalchemy import create_engine, text
import pandas as pd
import json
import os

# Load DB configuration
with open('config\db_config.json') as config_file:
    config = json.load(config_file)

DB_URI = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"

engine = create_engine(DB_URI)

# Create staging schema if not exists
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))
    conn.commit()

# Directory path for raw data
data_dir = 'Data/raw'

files = {
    'sales_2015': 'Sales_2015.csv',
    'sales_2016': 'Sales_2016.csv',
    'sales_2017': 'Sales_2017.csv',
    'territories': 'Territories.csv',
    'calendar': 'Calendar.csv',
    'customers': 'Customers.csv',
    'product_categories': 'Product_Categories.csv',
    'product_subcategories': 'Product_Subcategories.csv',
    'products': 'Products.csv',
    'returns': 'Returns.csv'
}

# Ingest data
for table_name, file_name in files.items():
    file_path = os.path.join(data_dir, file_name)
    print(f"Ingesting {file_name} into table {table_name}...")
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        continue
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError: Trying with ISO-8859-1 encoding for {file_name}")
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
    
    df.to_sql(table_name, con=engine, if_exists='append', index=False, schema='staging')
    print(f"{table_name} ingestion complete.")

print("All files ingested successfully.")
