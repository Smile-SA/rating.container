import sys
import yaml
import psycopg2
import json

def list_of_list(lst):
    if all(isinstance(item, list) for item in lst):
        return True
    elif all(not isinstance(item, list) for item in lst):
        return False
    else:
        return False


def insert_into_table(table_name,  columns,values):
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
        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))});"
        
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


def yaml_parser(yaml_file_path):    
    # Read the contents of the specified YAML file
    try:
        with open(yaml_file_path, 'r') as file:
            yaml_data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{yaml_file_path}' not found.")
        sys.exit(1)

    # Parse the YAML data
    try:
        data = yaml.safe_load(yaml_data)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    return data


def get_promql_from_yaml_parser(data):    
    # Extract variables from the 'spec' element
    spec = data.get('spec', {})

    # Get all keys in 'spec' before 'metric'
    variables = {}
    for key, value in spec.items():
        if key == 'metric':
            query = value
            break
        variables[key] = value

    # Replace placeholders in 'query' with corresponding variables
    for key, value in variables.items():
        placeholder = f'{{{key}}}'
        query = query.replace(placeholder, f'{{{value}}}')
    return query

