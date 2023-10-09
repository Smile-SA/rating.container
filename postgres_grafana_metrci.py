import requests
import json
import base64
import sys
# Grafana API URL (replace with your Grafana URL)
grafana_url = 'http://localhost:3000/api/dashboards/db'
dashboard_name = sys.argv[1]
metric_name = "process_cpu_seconds_total"# sys.argv[2]
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
                        "rawSql": f"SELECT time, temperature FROM sensor_data WHERE metric_name='{metric_name}'",
                        "interval": "1m",
                        
                    }
                ],
            },
            # Add more panels as needed
        ],

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
