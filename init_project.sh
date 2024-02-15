#!/bin/bash

# Set execute permissions for the scripts
chmod +x start-rating-docker.sh
chmod +x python-scripts/rating_rules_manager.py
chmod +x python-scripts/rating_results_to_json.py
chmod +x python-scripts/test_rating_results.py
chmod +x python-scripts/create_table.py
cp prometheus.yml /etc/prometheus
cp node_exporter.yml /etc/prometheus

# Run the create_table.py script
./python-scripts/create_table.py
