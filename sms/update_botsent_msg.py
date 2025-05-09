import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import json

# Database configuration
db_config = {
    'NAME': 'admin',
    'USER': 'postgres',
    'PASSWORD': 'Solution@97',
    'HOST': '217.145.69.172',
    'PORT': '5432'
}

# Function to safely strip strings (returns None if not a string)
def safe_strip(value):
    if isinstance(value, str):
        return value.strip()
    return value

# Function to safely convert dictionaries and lists to JSON strings
def safe_json(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value)  # Convert to JSON string
    return value

# Function to import data from CSV to PostgreSQL
def import_bot_sent_messages(csv_file, db_config):
    conn = None
    cursor = None
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)

        # Convert relevant columns to appropriate data types (JSON, DateTime, Decimal, etc.)
        df['contact_list'] = df['contact_list'].apply(lambda x: json.loads(x) if pd.notna(x) else [])
        df['button_data'] = df['button_data'].apply(lambda x: json.loads(x) if pd.notna(x) else {})
        df['product_data'] = df['product_data'].apply(lambda x: json.loads(x) if pd.notna(x) else {})
        df['sections'] = df['sections'].apply(lambda x: json.loads(x) if pd.notna(x) else [])
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        
        # Handle datetime conversion
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT']
        )
        cursor = conn.cursor()

        # Insert query
        insert_query = """
        INSERT INTO smsapp_botsentmessages (token, phone_number_id, contact_list, message_type, header, body, footer, 
                                            button_data, product_data, catalog_id, sections, latitude, longitude, media_id, created_at)
        VALUES %s
        ON CONFLICT (token, phone_number_id, message_type) DO NOTHING
        """

        # Prepare data for bulk insert
        data = []
        for _, row in df.iterrows():
            data.append((
                safe_strip(row['token']),
                safe_strip(row['phone_number_id']),
                safe_json(row['contact_list']),  # Convert to JSON string
                safe_strip(row['message_type']),
                safe_strip(row['header']) if pd.notna(row['header']) else None,
                safe_strip(row['body']),
                safe_strip(row['footer']) if pd.notna(row['footer']) else None,
                safe_json(row['button_data']),  # Convert to JSON string
                safe_json(row['product_data']),  # Convert to JSON string
                safe_strip(row['catalog_id']) if pd.notna(row['catalog_id']) else None,
                safe_json(row['sections']),  # Convert to JSON string
                row['latitude'],
                row['longitude'],
                safe_strip(row['media_id']) if pd.notna(row['media_id']) else None,
                row['created_at']
            ))

        # Execute bulk insert
        execute_values(cursor, insert_query, data)
        conn.commit()
        print(f"Successfully inserted {len(data)} records into BotSentMessages.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error during database insert: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # CSV file path
    csv_file = 'smsapp_botsentmessages.csv'  # Ensure the CSV is in the same directory as this script
    
    # Import data
    import_bot_sent_messages(csv_file, db_config)
