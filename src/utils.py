# utils.py
import json

def save_test_cases(test_cases, output_path):
    with open(output_path, 'w') as f:
        json.dump(test_cases, f, indent=4)

def load_test_cases(output_path):
    with open(output_path, 'r') as f:
        return json.load(f)
