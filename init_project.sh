#!/bin/bash

# Set execute permissions for the scripts
chmod +x start-rating-docker.sh
chmod +x python-scripts/rating_rules_manager.py
chmod +x python-scripts/rating_results_to_json.py
chmod +x python-scripts/test_rating_results.py
chmod +x python-scripts/create_table.py

# Check if /etc/prometheus directory exists
if [ ! -d "/etc/prometheus" ]; then
    # If not, create the directory and copy files
    mkdir /etc/prometheus        
fi
cp prometheus.yml /etc/prometheus
cp node_exporter.yml /etc/prometheus
# Install libpq-dev
sudo apt-get install libpq-dev
pip install -r requirements.txt
