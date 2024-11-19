#!/usr/bin/env python3
import psycopg2
import sys
import json


def res2json(table_name, metric_name, output_file):
    
    db_params = {
        'dbname': 'mydatabase',
        'user': 'myuser',
        'password': 'mypassword',
        'host': '0.0.0.0'  # Typically '0.0.0.0' for local connections
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
        select_sql = f"SELECT id, metric_name, metric_time, value FROM {table_name} WHERE metric_name='{metric_name}';" 

        # Execute the SELECT statement with the provided primary key values
        cursor.execute(select_sql)

        # Fetch the data for the specified composite primary key
        data = cursor.fetchall()

        if data:
            print("Data found:")
            # Fetch the column names
            col_names = [desc[0] for desc in cursor.description]

            # Combine column names with data in a dictionary
            data_with_columns = []
            for row in data:
                data_with_columns.append(dict(zip(col_names, row)))

            # Convert the data to a JSON object
            json_data = json.dumps(data_with_columns, default=str, indent=4)


            # Write the JSON data to a file
            with open(output_file, 'w') as f:
                f.write(json_data)
            print(f"Data written to {output_file} in JSON format.")
        else:
            print("Data not found for the specified composite primary key.")
    except psycopg2.Error as e:
        print(f"Error: Unable to fetch data: {e}")

    # Close the cursor and database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./rating_results_to_json.py  <metric_name> <output_file>")
        sys.exit(1)

    table_name = "metric_data" #sys.argv[1]
    metric_name = sys.argv[1]
    output_file = sys.argv[2]

    res2json(table_name, metric_name, output_file)
