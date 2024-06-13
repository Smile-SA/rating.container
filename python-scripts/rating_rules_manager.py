#!/usr/bin/env python3
import requests
import os
import sys
import yaml
from utils import insert_into_table
import json
import shutil
from utils import list_of_list
from utils import delete_from_table, extract_metric_name
from utils import create_instance
from utils import start_rating
from utils import update_custom_rules, get_prometheus_container, copy_rules_to_container, reload_prometheus_config, delete_custom_rules
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Prometheus Metric Script")
parser.add_argument("folder_path", nargs='?', default='./rating-rules', type=str, help="The path to the folder containing YAML files (default is current directory)")
parser.add_argument("--add", metavar="filename", type=str, help="Add a YAML file to the folder")
parser.add_argument("--rm", metavar="filename", type=str, help="Remove a YAML file from rating rules")
parser.add_argument("--update", metavar="filename", type=str, help="Update a YAML file from rating rules")

# Define either -t or --templates as options for templates path
parser.add_argument("-t", "--templates", metavar="/path/to/template(s)", type=str, help="Path to templates")

# Define either -v or --values as options for values path
parser.add_argument("-v", "--values", metavar="/path/to/value(s)", type=str, help="Path to values")

# Define either -i or --instance as options for instance path
parser.add_argument("-i", "--instance", metavar="/path/to/instance", type=str, help="Path to instance")

args = parser.parse_args()

folder_path = args.folder_path  # Get the folder path from the command line argument
if not os.path.isdir(folder_path):
    print(f"Error: {folder_path} is not a valid directory.")
    sys.exit(1)



if args.instance:
    
    # Assuming your create_instance function takes absolute paths
    template_path = os.path.abspath(args.templates) if args.templates else None
    value_path = os.path.abspath(args.values) if args.values else None
    instance_path = os.path.abspath(args.instance)
    
    # Call create_instance only if both templates and values paths are provided
    if template_path and value_path:
        print(f"Template Path: {args.templates}")
        print(f"Value Path: {args.values}")
        create_instance(template_path, value_path, instance_path)
        print(f"{args.instance} instance created")
        start_rating(instance_path)
        try:
            rules_file = "custom_rules.yml"
            update_custom_rules(args.add, rules_file)
            container_id = get_prometheus_container()
            copy_rules_to_container(container_id, rules_file)
            reload_prometheus_config(container_id)
            print("Updated custom rules and reloaded Prometheus configuration.")
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
    else:
        print("Both templates and values paths are required to create instances.")
    sys.exit(1)

if args.update:
    yaml_file_path = args.update
    start_rating(yaml_file_path)


if args.rm:
    yaml_file_path = args.rm #os.path.join(folder_path, args.rm)
    # Read the contents of the YAML file
    try:
        with open(yaml_file_path, 'r') as file:
            yaml_data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{yaml_file_path}' not found.")
        

    # Parse the YAML data
    try:
        data = yaml.safe_load(yaml_data)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")

    # Extract variables from the 'spec' element
    spec = data.get('spec', {})

    
    variables = {}
    for key, value in spec.items():
        if key == 'metric_name':
            metric_name = value
            break

    delete_from_table("metric_data","metric_name",metric_name)
    if os.path.exists(yaml_file_path):
        os.remove(yaml_file_path)
        print(f" {args.rm} Removed")
    rules_file = "custom_rules.yml"
    #metric_name = extract_metric_name(yaml_file_path)
    delete_custom_rules(metric_name, rules_file)
    container_id = get_prometheus_container()
    copy_rules_to_container(container_id, rules_file)
    reload_prometheus_config(container_id)

if args.add:
    # Code to add the YAML file specified by --add
    print(f"Adding {args.add} to {folder_path}/applied_instances")
    yaml_file_path = args.add
    if os.path.exists(yaml_file_path):
        # Construct the destination path in the folder
        destination_path = os.path.join(folder_path+"/applied_instances", os.path.basename(yaml_file_path))

        # Copy the file to the destination folder
        shutil.copy(yaml_file_path, destination_path)
        print(f"File {os.path.basename(yaml_file_path)} added to {folder_path}/applied_instances")
    else:
        print(f"Error: The specified file {yaml_file_path} does not exist.")

    start_rating(yaml_file_path)
    try:
        rules_file = "custom_rules.yml"
        update_custom_rules(args.add, rules_file)
        container_id = get_prometheus_container()
        copy_rules_to_container(container_id, rules_file)
        reload_prometheus_config(container_id)
        print("Updated custom rules and reloaded Prometheus configuration.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


    

if args.folder_path and not args.add and not args.rm and not args.update:

    for filename in os.listdir(folder_path):
        if filename.endswith('.yaml'):
            yaml_file_path = os.path.join(folder_path, filename)
            start_rating(yaml_file_path)
            


            

