#!/usr/bin/env python3
import requests
import sys
import yaml

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <yaml_file>")
    sys.exit(1)

# Get the YAML file path from the command-line argument
yaml_file_path = sys.argv[1]

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


# Define the Prometheus query expression
query_expression = 'go_memstats_alloc_bytes{job="prometheus"}[2m]'#query#'process_cpu_seconds_total{job="prometheus"}[2m]'
#your_metric
#cpu = "1"
#memory = "1"
#price = "0.5"
timeframe = "2m"




#query_expression = query_expression+'{job="prometheus"}'+f'[{timeframe}]'
print(query_expression)

# Define the Prometheus API URL
prometheus_url = 'http://localhost:9090/api/v1/query'

# Construct the request parameters
params = {
    'query': query_expression,
}

# Send the HTTP GET request to Prometheus
response = requests.get(prometheus_url, params=params)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    result = response.json()
    # Process the query result as needed
    print(result)
else:
    print(f"Failed to execute query. Status code: {response.status_code}")
