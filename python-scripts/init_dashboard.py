#!/usr/bin/env python3
import requests
import json
import base64
import sys
import subprocess

def get_prometheus_url():
    # Get the container ID of the Prometheus container
    container_id = subprocess.check_output(['sudo','docker', 'ps', '-q', '-f', 'name=prometheus']).decode('utf-8').strip()

    if not container_id:
        raise Exception('Prometheus container not found')

    # Get the IP address of the Prometheus container
    ip_address = subprocess.check_output(['sudo','docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', container_id]).decode('utf-8').strip()

    if not ip_address:
        raise Exception('Prometheus IP address not found')

    # Construct the Prometheus URL
    prometheus_url = f'http://{ip_address}:9090'
    return prometheus_url


# Define your Grafana API URL
grafana_url = 'http://localhost:3000'

# Define your Grafana username and password
username = 'admin'
password = 'admin'

# Define Prometheus as the data source (you may need to adjust this URL)
prometheus_datasource_url = get_prometheus_url()#'http://172.18.0.4:9090'

# Define your Prometheus queries
#prometheus_query_panel1 = '((ceil(sum(node_memory_Active_anon_bytes) * max(node_memory_MemTotal_bytes)/(1024*1024*1024))) + (ceil(sum(node_cpu_core_throttles_total)* max(node_cpu_package_throttles_total))) + sum(prometheus_remote_storage_samples_in_total)) * 220/1000 * 0.253 / 1000000'

#prometheus_query_panel2 = 'node_memory_Active_anon_bytes'

# Define the dashboard name
dashboard_name = 'carbon_dashboard'

# Create the Prometheus data source configuration
prometheus_datasource = {
    "name": "prometheus-ds2",  # Set the data source name as "prometheus"
    "type": "prometheus",
    "url": prometheus_datasource_url,
    "access": "proxy",
    "basicAuth": False,
    "isDefault": True,
}

# Define the panels configurations
panels = [
    {
        "title": "carbon_simulation_EU (KgCO2eq)",
        "query": "((ceil(sum(node_memory_Active_anon_bytes) * max(node_memory_MemTotal_bytes)/(1024*1024*1024)))\n    + (ceil(sum(prometheus_remote_storage_samples_in_total) * max(prometheus_remote_storage_samples_in_total)))\n    + sum(prometheus_remote_storage_samples_in_total)) * 220/1000 *0.238 / 1000000",
        "gridPos": {"x": 0, "y": 0, "w": 8, "h": 10},
    },
    {
        "title": "carbon_simulation_Germany (KgCO2eq)",
        "query": "((ceil(sum(node_memory_Active_anon_bytes) * max(node_memory_MemTotal_bytes)/(1024*1024*1024)))\n    + (ceil(sum(prometheus_remote_storage_samples_in_total) * max(prometheus_remote_storage_samples_in_total)))\n    + sum(prometheus_remote_storage_samples_in_total)) * 220/1000 *0.253 / 1000000",
        "gridPos": {"x": 8, "y": 0, "w": 8, "h": 10},
    },
    {
        "title": "carbon_simulation_France (KgCO2eq)",
        "query": "((ceil(sum(node_memory_Active_anon_bytes) * max(node_memory_MemTotal_bytes)/(1024*1024*1024)))\n    + (ceil(sum(prometheus_remote_storage_samples_in_total) * max(prometheus_remote_storage_samples_in_total)))\n    + sum(prometheus_remote_storage_samples_in_total)) * 220/1000 *0.28 / 1000000",
        "gridPos": {"x": 0, "y": 10, "w": 8, "h": 10},
    },
    {
        "title": "carbon_simulation_Italy (KgCO2eq)",
        "query": "((ceil(sum(node_memory_Active_anon_bytes) * max(node_memory_MemTotal_bytes)/(1024*1024*1024)))\n    + (ceil(sum(prometheus_remote_storage_samples_in_total) * max(prometheus_remote_storage_samples_in_total)))\n    + sum(prometheus_remote_storage_samples_in_total)) * 220/1000 *0.297 / 1000000",
        "gridPos": {"x": 8, "y": 10, "w": 8, "h": 10},
    },
]

# Create the dashboard configuration
dashboard_config = {
    "dashboard": {
        "title": dashboard_name,
        "panels": [],
    },
    "overwrite": True,
}

# Append panels to the dashboard configuration
for panel in panels:
    panel_config = {
        "type": "graph",
        "title": panel["title"],
        "datasource": 1,  # Use the Prometheus data source
        "targets": [
            {
                "expr": panel["query"],
                "legendFormat": "{{instance}}",
                "interval": "1m",
            }
        ],
        "gridPos": panel["gridPos"],
        "fieldConfig": {"unit": "percent"},
    }
    dashboard_config["dashboard"]["panels"].append(panel_config)

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