#!/bin/bash

# Start the containers
docker-compose up -d

# Wait for the containers to start properly (you may need to adjust the sleep time based on your setup)
sleep 4

# Retrieve the value of RULES_FOLDER from the rules_path.env file
source config.env
RULES_FOLDER_VALUE=$RULES_FOLDER

# Run the prometheus_metric.py script
./rating_rules_manager.py $RULES_FOLDER_VALUE


