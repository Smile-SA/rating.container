from flask import Flask, jsonify
import psycopg2
import sys
import json

app = Flask(__name__)

def read_data_from_table(table_name, metric_name=None):
    # Define your PostgreSQL database connection parameters
    db_params = {
        'dbname': 'mydatabase',
        'user': 'myuser',
        'password': 'mypassword',
        'host': 'localhost',
        'port': 5432  # Default PostgreSQL port is 5432
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
        if metric_name:
            select_sql = f"SELECT metric_name, metric_time, value FROM {table_name} WHERE metric_name='{metric_name}';"
        else : 
            select_sql = f"SELECT DISTINCT metric_name FROM {table_name};"
        # Execute the SELECT statement with the provided primary key values
        cursor.execute(select_sql)

        # Fetch the data for the specified composite primary key
        data = cursor.fetchall()

        if data:
            # Fetch the column names
            col_names = [desc[0] for desc in cursor.description]
            
            # Combine column names with data in a dictionary
            data_with_columns = []
            for row in data:
                data_with_columns.append(dict(zip(col_names, row)))
            
            json_data = json.dumps(data_with_columns, indent=2)[1:-1]
            #print(json_data)
            
            return  data_with_columns# json_data
        else:
            return None
    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()
@app.route('/')
def root():
    return '', 200 

@app.route('/query/<metric_name>')
def query(metric_name):
    table_name = 'metric_data'  # Replace with your actual table name
    if table_name and metric_name:
        data = read_data_from_table(table_name, metric_name)

        if data:
            return jsonify(data)#data
            res_json = jsonify(data)
            return res_json
        else:
            return jsonify({"error": "Data not found"})
    else:
        return jsonify({"error": "Missing parameters"})
    

@app.route('/metrics')
def metrics():
    table_name = 'metric_data'  # Replace with your actual table name
    
    if table_name:
        data = read_data_from_table(table_name)

        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "Data not found"})
    else:
        return jsonify({"error": "Missing parameters"})





if __name__ == '__main__':
    app.run(port=5000, debug=True)
