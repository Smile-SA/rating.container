#!/bin/bash

# Start the containers
docker-compose up -d

./python-scripts/create_table.py

# Retrieve the value of RULES_FOLDER from the rules_path.env file
source config.env
RULES_FOLDER_VALUE=$RULES_FOLDER
sleep 10
#
./python-scripts/rating_rules_manager.py $RULES_FOLDER_VALUE




