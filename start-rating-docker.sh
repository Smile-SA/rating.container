#!/bin/bash

# Start the containers
docker-compose up -d


# Retrieve the value of RULES_FOLDER from the rules_path.env file
source config.env
RULES_FOLDER_VALUE=$RULES_FOLDER

#
./python-scripts/rating_rules_manager.py $RULES_FOLDER_VALUE


