import sys
import psycopg2
import json
from collections import OrderedDict
import yaml
import requests


def start_rating(yaml_file_path,insert=True):
    yaml_data = None
    try:
        with open(yaml_file_path, 'r') as file:
            yaml_data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{yaml_file_path}' not found.")
    
    if yaml_data is None:
        return
        

    # Parse the YAML data
    try:
        data = yaml.safe_load(yaml_data)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")

    # Extract variables from the 'spec' element
    spec = data.get('spec', {})

    # Get all keys in 'spec' before 'metric'
    variables = {}
    for key, value in spec.items():
        if key == 'metric':
            query = value
        else:
            variables[key] = value

    # Replace placeholders in 'query' with corresponding variables
    for key, value in variables.items():
        placeholder = f'{{{key}}}'
        value_str = str(value)
        #query = query.replace(placeholder, f'{{{value}}}')
        query = query.replace(placeholder, value_str)
        
    query_expression = query
    
    # Define the Prometheus API URL
    prometheus_url = 'http://localhost:9090/api/v1/query'

    # Construct the request parameters
    params = {

        'query' : query_expression,

    }

    # Send the HTTP GET request to Prometheus
    response = requests.get(prometheus_url, params=params)
    if insert:    
        table_name = "metric_data"
        columns = ['metric_name','job_name','metric_time','value']
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            result = response.json()
            if result['data']['result']:
                
                
                for item in result['data']['result']:
                    #print(item)
                    #job = item['metric']['job']
                    job = item['metric']
                    values = item['value']
                    if list_of_list(values):    
                        for val in values:
                            all_data = [query_expression,"",val[0],val[1]]
                            insert_into_table(table_name,columns, all_data)
                            
                            
                    else:
                        all_data = [query_expression,"",values[0],values[1]]
                        insert_into_table(table_name, columns, all_data)
                        

            else : 
                print(f" {yaml_file_path} : rules are not applicable")        
        else:
            print(f"Failed to execute query. Status code: {response.status_code}")
        return 
    else:
        return response
    

def create_instance(template_path, value_path, instance_path):
    # Load the template and value YAML files
    with open(template_path, 'r') as template_file:
        template_data = yaml.safe_load(template_file)

    with open(value_path, 'r') as value_file:
        value_data = yaml.safe_load(value_file)

    # Assuming value_data is a list of dictionaries
    if isinstance(value_data, list):
        # Merge dictionaries in the list
        merged_dict = {}
        for d in value_data:
            merged_dict.update(d)
        value_data = merged_dict

    # Ensure that value_data is a dictionary
    if not isinstance(value_data, dict):
        print(f"Error: Invalid format in {value_path}")
        return

    content_instance = OrderedDict((key, value_data[key]) for key in value_data.keys())
    content_instance['metric'] = template_data['spec']['query_template']
    
    # Convert OrderedDict to regular dictionary
    content_instance_dict = dict(content_instance)


    # Create the instance YAML data
    instance_data = {
        'apiVersion': 'rating.alterway.fr/v1',
        'kind': 'RatingRuleInstance',
        'metadata': {
            'name': f'rating-rule-instance-{content_instance["metric_name"]}',
            'namespace': 'rating'
        },
        'spec': content_instance_dict
    }

    # Write the instance YAML data to the instance file
    with open(instance_path, 'w') as instance_file:
        yaml.dump(instance_data, instance_file, default_flow_style=False)

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
        #print("Data inserted successfully.")
    except psycopg2.Error as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"Error: Unable to insert data: {e}")
    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()



def delete_from_table(table_name, column, value_of_column):
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
        # Construct the SQL DELETE statement dynamically
        delete_sql = f"DELETE FROM {table_name} WHERE {column} = %s;"
        
        # Execute the DELETE statement with the provided value
        cursor.execute(delete_sql, (value_of_column,))
        
        # Commit the transaction to save the changes
        conn.commit()
        #print("Data deleted successfully.")
    except psycopg2.Error as e:
        # Rollback the transaction in case of an error
        conn.rollback()
        print(f"Error: Unable to delete data: {e}")
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



#query_expression = f'{query}{{job="prometheus"}}[{timeframe}]'

#query_expression = "url_access_count_total"
#print(query)
#query_expression = query+'{job="prometheus"}'+f'[{timeframe}]'
#print(query_expression)