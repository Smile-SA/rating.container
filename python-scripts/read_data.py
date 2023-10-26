import psycopg2
import sys

def read_data_from_table(table_name):
    # Define your PostgreSQL database connection parameters
    db_params = {
        'dbname': 'mydatabase',
        'user': 'myuser',
        'password': 'mypassword',
        'host': 'localhost'  # Typically 'localhost' for local connections
                            # Default PostgreSQL port is 5432
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
        # Construct the SQL SELECT statement dynamically for composite primary keys
        select_sql = f"SELECT * FROM {table_name} ;"
        
        # Execute the SELECT statement with the provided primary key values
        cursor.execute(select_sql)
        
        # Fetch the data for the specified composite primary key
        data = cursor.fetchall()
        
        if data:
            print("Data found:")
            print(data)
        else:
            print("Data not found for the specified composite primary key.")
    except psycopg2.Error as e:
        print(f"Error: Unable to fetch data: {e}")

    # Close the cursor and database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_from_table.py <table_name> <primary_key_value1> <primary_key_value2> ...")
        sys.exit(1)
    
    table_name = sys.argv[1]
    #primary_key_values = sys.argv[2:]
    
    read_data_from_table(table_name)
