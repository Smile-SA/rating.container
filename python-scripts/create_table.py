#!/usr/bin/env python3

import psycopg2
from psycopg2 import sql

def create_metric_data_table(db_params):
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(**db_params)
    
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    
    # Define the SQL statement to create the metric_data table
    create_table_query = """
    CREATE TABLE metric_data (
        id SERIAL PRIMARY KEY,
        metric_name TEXT,
        prom_query TEXT NOT NULL,
        job_name TEXT,
        metric_time REAL,
        value TEXT
    );
    """
    
    try:
        # Execute the SQL statement to create the table
        cursor.execute(create_table_query)
        
        # Commit the changes to the database
        connection.commit()
        print("Table 'metric_data' created successfully.")
    except Exception as e:
        # Rollback the changes if an error occurs
        connection.rollback()
        print(f"Error creating table: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


if __name__ == "__main__":
    db_params = {
        'dbname': 'mydatabase',
        'user': 'myuser',
        'password': 'mypassword',
        'host': '0.0.0.0',
        #'port': '5432' Default PostgreSQL port is 5432
    }

    create_metric_data_table(db_params)
