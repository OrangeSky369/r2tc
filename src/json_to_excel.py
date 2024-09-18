import json
import pandas as pd

def json_to_excel(json_file_path, excel_file_path):
    """
    Converts a JSON file containing test cases into an Excel file.
    Only the first step of each test case will have test_case_name, precondition, and linked_req filled.
    Subsequent steps will have these cells left empty.

    Parameters:
    - json_file_path: str, path to the input JSON file.
    - excel_file_path: str, path to the output Excel file.
    """
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        test_cases = json.load(file)

    # List to hold all rows for the Excel file
    excel_rows = []

    for test_case in test_cases:
        test_case_name = test_case.get("test_case_name", "")
        precondition = test_case.get("precondition", "")
        linked_req = ", ".join(test_case.get("linked_req", []))
        test_steps = test_case.get("test_steps", [])

        for idx, step in enumerate(test_steps):
            step_number = step.get("step_number", "")
            test_step = f"Step {step_number}"
            step_description = step.get("description", "")
            expected_result = step.get("expected_result", "")

            # Only fill test_case_name, precondition, and linked_req for the first step
            if idx == 0:
                row = {
                    "test_case_name": test_case_name,
                    "precondition": precondition,
                    "test_step": test_step,
                    "step_description": step_description,
                    "expected_result": expected_result,
                    "linked_req": linked_req
                }
            else:
                row = {
                    "test_case_name": "",
                    "precondition": "",
                    "test_step": test_step,
                    "step_description": step_description,
                    "expected_result": expected_result,
                    "linked_req": ""
                }

            excel_rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(excel_rows, columns=[
        "test_case_name",
        "precondition",
        "test_step",
        "step_description",
        "expected_result",
        "linked_req"
    ])

    # Write to Excel
    df.to_excel(excel_file_path, index=False, engine='openpyxl')
    print(f"Successfully converted {json_file_path} to {excel_file_path}")
