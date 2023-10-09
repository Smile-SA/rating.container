#!/usr/bin/env python3
import requests
import json
import base64
import sys

#up == 1

# Define your Grafana API URL
grafana_url = 'http://localhost:3000'

# Define your Grafana username and password
username = 'admin'
password = 'Password!!777'

# Define Prometheus as the data source (you may need to adjust this URL)
prometheus_datasource_url = 'http://prometheus:9090'

# Define your Prometheus queries
prometheus_query = 'process_cpu_seconds_total'  # Replace with your specific Prometheus query
#prometheus_query = 'node_memory_MemTotal_bytes'
#prometheus_query = 'go_memstats_alloc_bytes'
# Define the dashboard name as a command-line argument
dashboard_name = sys.argv[1]

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
    "title": "CPU Usage",#"MemStats",#"MemTotal_bytes",#
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
else:
    print(f'Failed to create dashboard. Status code: {response_dashboard.status_code}')
    print(response_dashboard.text)
