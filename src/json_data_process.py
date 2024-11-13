import json


def aggregate_requirements(requirements):
    """
    Aggregate requirements based on the parentBinding field.
    Use the parent's '主文本' (identified by '标识') as the group name and function module.
    :param requirements: requirements in json format
    :return: list of aggregated requirements
    """
    # Creating a mapping from 标识 to 主文本 for quick lookup
    id_to_text = {req['标识']: req['主文本'] for req in requirements}

    # Dictionary to hold aggregated requirements
    aggregate_requirements = {}

    # Iterate through each requirement
    for req in requirements:
        parent_id = req['parentBinding']
        if parent_id in id_to_text:
            # Use the parent's 主文本 as the group name and function module
            function_module = id_to_text[parent_id]

            # Initialize the group if it doesn't exist
            if function_module not in aggregate_requirements:
                aggregate_requirements[function_module] = {
                    "function_module": function_module,
                    "requirements": []
                }

            # Add the requirement to the appropriate group
            aggregate_requirements[function_module]["requirements"].append(req)

    # Convert the aggregated dictionary to a list for easier processing
    return list(aggregate_requirements.values())


# Save generated test cases to json file
def save_test_cases_json(str_test_cases, output_json_path):
    # Remove the enclosing triple backticks and the `json` language identifier
    str_test_cases = str_test_cases.strip()
    if str_test_cases.startswith('```json'):
        str_test_cases = str_test_cases[7:-4].strip()

    # Parse the cleaned string content into a JSON object
    json_content = json.loads(str_test_cases)

    # Write the JSON object to the specified output file
    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(json_content, file, ensure_ascii=False, indent=4)

    print(f"Test cases already saved in JSON file: {output_json_path}")
