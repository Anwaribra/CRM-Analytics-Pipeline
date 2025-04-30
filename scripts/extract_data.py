import os
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# Database connection
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'crm_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

# Create database connection
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def create_schemas():
    """Create necessary schemas if they don't exist"""
    schemas = ['raw', 'staging', 'marts']
    with engine.connect() as conn:
        for schema in schemas:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema}'))
        conn.commit()

def extract_customers():
    """Extract customer data from source and load to raw schema"""
    customers_data = pd.DataFrame({
        'id': range(1, 101),
        'first_name': [f'Customer_{i}' for i in range(1, 101)],
        'last_name': [f'Last_{i}' for i in range(1, 101)],
        'email': [f'customer_{i}@example.com' for i in range(1, 101)],
        'phone': [f'123-456-{i:04d}' for i in range(1, 101)],
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    })
    
    customers_data.to_sql('customers', engine, schema='raw', if_exists='replace', index=False)

def extract_orders():
    """Extract order data from source and load to raw schema"""
    orders_data = pd.DataFrame({
        'id': range(1, 201),
        'customer_id': [i % 100 + 1 for i in range(200)],  
        'order_date': pd.date_range(start='2023-01-01', periods=200),
        'status': ['completed'] * 200,
        'total_amount': [100.0 * (i % 10 + 1) for i in range(200)],
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    })
    
    orders_data.to_sql('orders', engine, schema='raw', if_exists='replace', index=False)

if __name__ == '__main__':
    print("Creating schemas...")
    create_schemas()
    print("Starting data extraction...")
    extract_customers()
    extract_orders()
    print("Data extraction completed successfully!") 