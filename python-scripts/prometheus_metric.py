#!/usr/bin/env python3
import requests
import os
import sys
import yaml
from utils import insert_into_table
import json
import shutil
from utils import list_of_list
from utils import delete_from_table
import argparse


# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Prometheus Metric Script")
parser.add_argument("folder_path", nargs='?', default='./rules_folder', type=str, help="The path to the folder containing YAML files (default is current directory)")
parser.add_argument("--add", metavar="filename", type=str, help="Add a YAML file to the folder")
parser.add_argument("--rm", metavar="filename", type=str, help="Remove a YAML file from rating rules")
parser.add_argument("--update", metavar="filename", type=str, help="Update a YAML file from rating rules")

args = parser.parse_args()

folder_path = args.folder_path  # Get the folder path from the command line argument
if not os.path.isdir(folder_path):
    print(f"Error: {folder_path} is not a valid directory.")
    sys.exit(1)

if args.update:
    yaml_file_path = args.update

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

 

    # Define the Prometheus API URL
    prometheus_url = 'http://localhost:9090/api/v1/query'

    # Construct the request parameters
    params = {

        'query' : query_expression,

    }

    # Send the HTTP GET request to Prometheus
    response = requests.get(prometheus_url, params=params)

    table_name = "metric_data"
    columns = ['metric_name','job_name','metric_time','value']
    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        result = response.json()
        if result['data']['result']:
            print(yaml_file_path)
            print(result)
            for item in result['data']['result']:
                #print(item)
                #job = item['metric']['job']
                job = item['metric']
                values = item['value']
                if list_of_list(values):    
                    for val in values:
                        all_data = [query_expression,"",val[0],val[1]]
                        insert_into_table(table_name,columns, all_data)
                        
                        
                else:
                    all_data = [query_expression,"",values[0],values[1]]
                    insert_into_table(table_name, columns, all_data)
                    

        else : 
            print(f" {yaml_file_path} : rules are not applicable")        
    else:
        print(f"Failed to execute query. Status code: {response.status_code}")



if args.rm:
    yaml_file_path = os.path.join(folder_path, args.rm)
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
        
    else:
        print(f"File {args.rm} not found in {folder_path}")

    delete_from_table("metric_data","metric_name",query)
    if os.path.exists(yaml_file_path):
        os.remove(yaml_file_path)
        print(f"Removed {args.rm} from {folder_path}")

if args.add:
    # Code to add the YAML file specified by --add
    print(f"Adding {args.add} to {folder_path}")
    yaml_file_path = args.add
    if os.path.exists(yaml_file_path):
        # Construct the destination path in the folder
        destination_path = os.path.join(folder_path, os.path.basename(yaml_file_path))

        # Copy the file to the destination folder
        shutil.copy(yaml_file_path, destination_path)
        print(f"File {os.path.basename(yaml_file_path)} added to {folder_path}")
    else:
        print(f"Error: The specified file {yaml_file_path} does not exist.")

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

 

    # Define the Prometheus API URL
    prometheus_url = 'http://localhost:9090/api/v1/query'

    # Construct the request parameters
    params = {

        'query' : query_expression,

    }

    # Send the HTTP GET request to Prometheus
    response = requests.get(prometheus_url, params=params)

    table_name = "metric_data"
    columns = ['metric_name','job_name','metric_time','value']
    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        result = response.json()
        if result['data']['result']:
            print(yaml_file_path)
            print(result)
            for item in result['data']['result']:
                #print(item)
                #job = item['metric']['job']
                job = item['metric']
                values = item['value']
                if list_of_list(values):    
                    for val in values:
                        all_data = [query_expression,"",val[0],val[1]]
                        insert_into_table(table_name,columns, all_data)
                        
                        
                else:
                    all_data = [query_expression,"",values[0],values[1]]
                    insert_into_table(table_name, columns, all_data)
                    

        else : 
            print(f" {yaml_file_path} : rules are not applicable")        
    else:
        print(f"Failed to execute query. Status code: {response.status_code}")



if args.folder_path and not args.add and not args.rm and not args.update:

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

            # Define the Prometheus API URL
            prometheus_url = 'http://localhost:9090/api/v1/query'

            # Construct the request parameters
            params = {

                'query' : query_expression,

            }

            # Send the HTTP GET request to Prometheus
            response = requests.get(prometheus_url, params=params)

            table_name = "metric_data"
            columns = ['metric_name','job_name','metric_time','value']
            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                result = response.json()
                if result['data']['result']:
                    print(filename)
                    print(result)
                    for item in result['data']['result']:
                        #print(item)
                        #job = item['metric']['job']
                        job = item['metric']
                        values = item['value']
                        if list_of_list(values):    
                            for val in values:
                                all_data = [query_expression,"",val[0],val[1]]
                                insert_into_table(table_name,columns, all_data)
                                
                                
                        else:
                            all_data = [query_expression,"",values[0],values[1]]
                            insert_into_table(table_name, columns, all_data)
                            

                else : 
                    print(f" {filename} : rules are not applicable")        
            else:
                print(f"Failed to execute query. Status code: {response.status_code}")
                

