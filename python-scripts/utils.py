import sys
import yaml
import psycopg2
import json
from collections import OrderedDict
import yaml
import requests
import subprocess

def start_rating(yaml_file_path,insert=True):
    try:
        with open(yaml_file_path, 'r') as file:
            yaml_data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{yaml_file_path}' not found.")
    
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
            
        variables[key] = value

    # Replace placeholders in 'query' with corresponding variables
    for key, value in variables.items():
        placeholder = f'{{{key}}}'
        value_str = str(value)
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
        columns = ['metric_name','prom_query','job_name','metric_time','value']
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            result = response.json()
            if result['data']['result']:
                
                
                for item in result['data']['result']:
                    job = item['metric']
                    values = item['value']
                    if list_of_list(values):    
                        for val in values:
                            all_data = [variables['metric_name'],query_expression,"",val[0],val[1]]
                            insert_into_table(table_name,columns, all_data)
                            
                            
                    else:
                        all_data = [variables['metric_name'],query_expression,"",values[0],values[1]]
                        insert_into_table(table_name, columns, all_data)
                        

            else : 
                print(f" {yaml_file_path} : rules are not applicable")        
        else:
            print(f"Failed to execute query. Status code: {response.status_code}")
        return 
    else:
        return response.json()


def create_instance(template_path, value_path, instance_path):
    try:
        # Load the template and value YAML files
        with open(template_path, 'r') as template_file:
            template_data = yaml.safe_load(template_file)

        with open(value_path, 'r') as value_file:
            value_data = yaml.safe_load(value_file)
    except Exception as e:
        print(f"Error loading YAML files: {e}")
        return

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

    try:
        # Replace {carbon_factor} placeholder in query_template with the actual value
        if 'carbon_factor' in value_data and 'query_template' in template_data['spec']:
            query_template = template_data['spec']['query_template']
            query_template = query_template.replace('{carbon_factor}', str(value_data['carbon_factor']))
            template_data['spec']['query_template'] = query_template
        
        # Create content instance from value_data
        content_instance = OrderedDict((key, value_data[key]) for key in value_data.keys())
        content_instance['metric'] = template_data['spec']['query_template']
    
        # Convert OrderedDict to regular dictionary
        content_instance_dict = dict(content_instance)

        # Create the instance YAML data
        instance_data = {
            'apiVersion': 'rating.smile.fr/v1',
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

        print(f"Instance YAML file created at {instance_path}")
    
    except KeyError as e:
        print(f"Error: Missing key in the provided data - {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

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

def update_custom_rules(input_file, rules_file):
    # Read the input YAML file
    with open(input_file, 'r') as file:
        input_data = yaml.safe_load(file)
    
    # Extract the necessary fields from the input YAML
    name = input_data['spec']['metric_name']
    expr = input_data['spec']['metric']
    
    # Create the new rule to be added
    new_rule = {
        'record': name,
        'expr': expr
    }
    
    # Read the existing rules file
    with open(rules_file, 'r') as file:
        rules_data = yaml.safe_load(file)
    
    # Add the new rule to the rules data
    rules_data['groups'][0]['rules'].append(new_rule)
    
    # Write the updated rules back to the file
    with open(rules_file, 'w') as file:
        yaml.dump(rules_data, file, default_flow_style=False)
    
    #print(f"Updated {rules_file} with new rule for {name}")

def get_prometheus_container():
    # Find the Prometheus container ID
    result = subprocess.run(['sudo','docker', 'ps', '--filter', 'ancestor=quay.io/prometheus/prometheus:v2.33.1', '--format', '{{.ID}}'],
                            stdout=subprocess.PIPE, text=True, check=True)
    container_id = result.stdout.strip()
    if not container_id:
        raise RuntimeError("Prometheus container not found!")
    return container_id

def copy_rules_to_container(container_id, rules_file):
    # Extract filename from the full path
    rules_filename = rules_file.split('/')[-1]
    # Copy the updated custom rules file to the Prometheus container
    subprocess.run(['sudo','docker', 'cp', rules_file, f'{container_id}:/etc/prometheus/{rules_filename}'], check=True)

def reload_prometheus_config(container_id):
    # Reload Prometheus configuration by sending SIGHUP signal
    subprocess.run(['sudo','docker', 'kill', '-s', 'HUP', container_id], check=True)

def delete_custom_rules(record_name, rules_file):
    with open(rules_file, 'r') as file:
        data = yaml.safe_load(file)

    modified = False
    for group in data['groups']:
        initial_rule_count = len(group['rules'])
        group['rules'] = [rule for rule in group['rules'] if rule.get('record') != record_name]
        if len(group['rules']) != initial_rule_count:
            modified = True

    if modified:
        with open(rules_file, 'w') as file:
            yaml.safe_dump(data, file, default_flow_style=False)
        print(f"Deleted rule '{record_name}' from {rules_file}.")
    else:
        print(f"No rule with record name '{record_name}' found in {rules_file}.")

def extract_metric_name(yaml_file_path):
    try:
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File '{yaml_file_path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

    spec = data.get('spec', {})
    metric_name = spec.get('metric_name')

    if metric_name:
        return metric_name
    else:
        print("Metric name not found in the YAML file.")
        return None