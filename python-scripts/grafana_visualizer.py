#!/usr/bin/env python3
import requests
import json
import base64
import sys
import yaml
import os

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

    
        query_expression = query

        # Grafana API URL (replace with your Grafana URL)
        grafana_url = 'http://localhost:3000/api/dashboards/db'

        metric_name = query_expression
        dashboard_name = "dashboard "+ metric_name
        # Define the Grafana dashboard configuration
        dashboard_config = {
            "dashboard": {
                "id": None,  # Set to None for a new dashboard
                "title": dashboard_name,
                "panels": [
                    {
                        "title": "Panel 1",
                        "type": "graph",
                        "datasource": "PostgreSQL",  # Make sure this matches your configured datasource
                        "targets": [
                            {
                                "refId": "A",
                                "rawSql": f"SELECT time,value FROM metric_data WHERE metric_name='{metric_name}'",
                                
                            }
                        ],
                    },
                    # Add more panels as needed
                ],
                "time": {
                    "from": "now-5h",
                    "to": "now",
                },
            },
            "folderId": 0,  # Set to the desired folder ID or create a new folder
            "overwrite": True,  # Set to True to overwrite an existing dashboard with the same title
        }

        # Encode the username and password for basic authentication
        username = 'admin'
        password = 'Password!!777'
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

        # Create the dashboard using basic authentication headers
        headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/json',
        }

        # Send a POST request to create the dashboard
        response = requests.post(grafana_url, headers=headers, json=dashboard_config)

        # Check if the request was successful and parse the JSON response
        if response.status_code == 200:
            response_json = response.json()
            if 'id' in response_json:
                print(f"Dashboard created successfully with ID: {response_json['id']}")
            else:
                print("Dashboard creation succeeded, but the ID was not provided in the response.")
        else:
            print(f"Failed to create dashboard. Status code: {response.status_code}")
