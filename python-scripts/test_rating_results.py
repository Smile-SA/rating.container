#!/usr/bin/env python3

from utils import start_rating
import sys

def check_rating_result(result, inf_threshold, sup_threshold):
    if 'status' in result and result['status'] == 'success':
        if 'data' in result and 'resultType' in result['data'] and 'result' in result['data']:
            metric_result = result['data']['result'][0]  # Assuming there's only one result in the vector
            values = metric_result.get('value', [])
            
            if values:
                timestamp, metric_value = values
                # Convert the metric_value to a float for comparison
                metric_float = float(metric_value)
                
                # Check if the metric value is within the specified range
                assert inf_threshold <= metric_float <= sup_threshold, "Rating result outside the acceptable range"
                
                # Return True if the assertion passes
                return True

    # Raise AssertionError if any of the conditions fail
    raise AssertionError("Invalid or incomplete result structure")


def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <yaml_file_path> <inf_threshold> <sup_threshold>")
        sys.exit(1)

    yaml_file_path = sys.argv[1]
    inf_threshold = float(sys.argv[2])
    sup_threshold = float(sys.argv[3])

    result = start_rating(yaml_file_path, insert=False)

    try:
        # Check if the rating result is within the specified range
        assert check_rating_result(result, inf_threshold, sup_threshold), \
            f"Rating result outside the acceptable range ({inf_threshold} - {sup_threshold})."
        
        print(f"Rating result is within the acceptable range ({inf_threshold} - {sup_threshold}).")
        # Additional processing or validation can be added here
    except AssertionError as e:
        print(e)

if __name__ == "__main__":
    main()
