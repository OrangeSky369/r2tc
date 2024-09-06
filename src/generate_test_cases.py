from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json
import os

def aggregate_requirements(requirements):
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

def generate_test_cases(model_name, aggregated_requirements):
    # Initialize Ollama model using langchian
    model = OllamaLLM(model=model_name)

    test_cases = []

    # Process each group of aggregated requirements
    for group in aggregated_requirements:
        function_module = group['function_module']
        requirements_text = "\n".join(f"- {req['主文本']}" for req in group['requirements'])

        template = """
                Action: {action}
                        
                Generate all relevant test cases. Each test case should include:
                - A descriptive test case name
                - Precondition
                - Multiple test steps, each with a description and expected result
                - Function module
                
                Output format should be in JSON, with each test case structured as follows:
                {{
                    "test_case_name": "<Test case name>",
                    "precondition": "<Precondition>",
                    "test_steps": [
                        {{
                            "step_number": <Step Number>
                            "description": "<Step description>",
                            "expected_result": "<Expected result>"
                        }},
                        ...
                    ],
                    "function_module": "<function_module>"
                }}"""

        prompt = ChatPromptTemplate.from_template(template)

        chain = prompt | model

        response = chain.invoke({"action": f"Given the following requirements: {requirements_text}, generate the test cases for {function_module}."})
        # print(type(response))
        # print(response)
        return response
        # Generate test cases using Ollama
        # response = llm.generate(prompt)
        # test_cases_group = json.loads(response)
        # test_cases.extend(response)

# Save generated test cases to json file
def save_test_cases_json(str_test_cases, output_json_path):
    # Remove the enclosing triple backticks and the `json` language identifier
    if str_test_cases.startswith('```json'):
        str_test_cases = str_test_cases[7:-3].strip()

    # Parse the cleaned string content into a JSON object
    json_content = json.loads(str_test_cases)

    # Write the JSON object to the specified output file
    with open(output_json_path, 'w', encoding='utf-8') as file:
        json.dump(json_content, file, ensure_ascii=False, indent=4)

    print(f"Test cases already saved in JSON file: {output_json_path}")
