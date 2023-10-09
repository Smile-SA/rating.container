import psycopg2
import sys

def insert_into_table(table_name, values):
    # Define your PostgreSQL database connection parameters
    db_params = {
        'dbname': 'mydatabase',
        'user': 'myuser',
        'password': 'mypassword',
        'host': 'localhost'  # Typically 'localhost' for local connections
        #'port': 'your_port'   # Default PostgreSQL port is 5432
    }

    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(**db_params)
    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database: {e}")
        sys.exit(1)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Construct the SQL INSERT statement dynamically
        insert_sql = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(values))});"
        
        # Execute the INSERT statement with the provided values
        cursor.execute(insert_sql, values)
        
        # Commit the transaction to save the changes
        conn.commit()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"Error: Unable to insert data: {e}")
    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python insert_into_table.py <table_name> <value1> <value2> ...")
        sys.exit(1)
    
    table_name = sys.argv[1]
    values = sys.argv[2:]
    
    insert_into_table(table_name, values)
#'2023-08-30 12:00:00', 'Metric2', '123', 'Var2', 'Template2'
#metric