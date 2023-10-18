import requests
import os
import sys
import yaml
from utils import insert_into_table


# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <yaml_file>")
    sys.exit(1)

folder_path = sys.argv[1]  # Get the folder path from the command line
if not os.path.isdir(folder_path):
    print(f"Error: {folder_path} is not a valid directory.")
    sys.exit(1)


for filename in os.listdir(folder_path):
    if filename.endswith('.yaml'):
        yaml_file_path = os.path.join(folder_path, filename)

        # Read the contents of the YAML file
        try:
            with open(yaml_file_path, 'r') as file:
                yaml_data = file.read()
        except FileNotFoundError:
            print(f"Error: File '{yaml_file_path}' not found.")
            continue

        # Parse the YAML data
        try:
            data = yaml.safe_load(yaml_data)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            continue

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

        timeframe = "2m"


        #query_expression = f'{query}{{job="prometheus"}}[{timeframe}]'
        query_expression = query
        print(query)
        #query_expression = query_expression+'{job="prometheus"}'+f'[{timeframe}]'
        #print(query_expression)

        # Define the Prometheus API URL
        prometheus_url = 'http://localhost:9090/api/v1/query'

        # Construct the request parameters
        params = {

            'query' : query_expression,

        }

        # Send the HTTP GET request to Prometheus
        response = requests.get(prometheus_url, params=params)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            result = response.json()
            # Process the query result as needed
            print(result)
            table_name = 'sensor_data'
            insert_into_table(table_name, result['value'])
            
        else:
            print(f"Failed to execute query. Status code: {response.status_code}")
