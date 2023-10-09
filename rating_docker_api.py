from flask import Flask, jsonify
import yaml
import requests
import sys
import yaml
import base64
import json

app = Flask(__name__)


@app.route('/prometheus', methods=['GET'])
def get_data():
    # Read the contents of the specified YAML file
    yaml_file_path = 'rating_rules.yaml'
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
    query_expression = query#'go_memstats_alloc_bytes{job="prometheus"}[2m]'#query#'process_cpu_seconds_total{job="prometheus"}[2m]'
    timeframe = "3600s"
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
    result = []
    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        result = response.json()
        # Process the query result as needed
        print(result)
    else:
        print(f"Failed to execute query. Status code: {response.status_code}")
    return result

# Define a new route for the /grafana endpoint
@app.route('/grafana', methods=['GET'])
def get_grafana_data():
    # Read and parse the YAML file for Grafana data
    #with open('grafana_data.yaml', 'r') as yaml_file:
    #    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    #return jsonify(data)
    grafana_url = 'http://localhost:3000'

    # Define your Grafana username and password
    username = 'admin'
    password = 'Password!!777'

    # Define Prometheus as the data source (you may need to adjust this URL)
    prometheus_datasource_url = 'http://prometheus:9090'

    # Define your Prometheus queries
    prometheus_query = 'node_memory_MemTotal_bytes'  # Replace with your specific Prometheus query
    #prometheus_query = 'node_memory_MemTotal_bytes'
    #prometheus_query = 'go_memstats_alloc_bytes'
    # Define the dashboard name as a command-line argument
    dashboard_name = "Dashboard API"

    # Create the Prometheus data source configuration
    prometheus_datasource = {
        "name": "my-prometheus",  # Set the data source name as "prometheus"
        "type": "prometheus",
        "url": prometheus_datasource_url,
        "access": "proxy",
        "basicAuth": False,
        "isDefault": True,
    }

    # Define the CPU Usage panel configuration
    cpu_usage_panel = {
        "type": "graph",
        "title": "API",#"MemStats",#"MemTotal_bytes",#
        "datasource":  1 ,  # Use the Prometheus data source
        "targets": [
            {
                "expr": prometheus_query,  # Use your Prometheus query here
                "legendFormat": "{{instance}}",
                "interval": "1m",
            }
        ],
        "gridPos": {  # Adjust the size and position here
            "x": 0,    # Horizontal position (0 is the leftmost column)
            "y": 0,    # Vertical position (0 is the top row)
            "w": 8,   # Width (number of columns)
            "h": 10     # Height (number of rows)
        },
        "fieldConfig": {
            "unit": "percent"
        }
    }

    # Create the dashboard configuration
    dashboard_config = {
        "dashboard": {
            "title": dashboard_name,
            "panels": [cpu_usage_panel],
        },
        "overwrite": True,
    }

    # Encode the username and password for basic authentication
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

    # Create the dashboard using basic authentication headers
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json',
    }


    # Create the Prometheus data source
    response_datasource = requests.post(f'{grafana_url}/api/datasources', data=json.dumps(prometheus_datasource), headers=headers)

    if response_datasource.status_code == 200:
        print('Prometheus data source created successfully!')
    else:
        print(f'Failed to create Prometheus data source. Status code: {response_datasource.status_code}')
        print(response_datasource.text)

    # Create the dashboard
    response_dashboard = requests.post(f'{grafana_url}/api/dashboards/db', data=json.dumps(dashboard_config), headers=headers)

    if response_dashboard.status_code == 200:
        print('Dashboard created successfully!')
        print(response_dashboard.json())
        return "Dashboard created successfully!\n"
    else:
        print(f'Failed to create dashboard. Status code: {response_dashboard.status_code}')
        print(response_dashboard.text)
    return 'None'




if __name__ == '__main__':
    app.run(debug=True)
