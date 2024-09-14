from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json
import os

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

def generate_test_cases(model_name, aggregated_requirements):
    # Initialize Ollama model using langchian
    model = OllamaLLM(model=model_name)

    test_cases = []

    # Process each group of aggregated requirements
    for group in aggregated_requirements:
        function_module = group['function_module']
        requirements_text = "\n".join([f"- {req['主文本']}" for req in group['requirements']])
        # requirements_text = "\n".join(f"- {req['主文本']}" for req in group['requirements'])
        requirement_ids = [req['标识'] for req in group['requirements']]  # list of IDs for linked_req

        template = """
                Action: {action}
                
                以下是测试用例生成要求：
                     
                为需求中"验证方法Verification Method"参数为"HIL"，且"工件类型"参数为"Requirement"的需求生成测试用例。每条测试用例应包含：
                - 一个描述性的用例名称
                - 前置条件
                - 若干测试步骤，每个测试步骤都包含描述和预期结果
                - 功能模块
                - 链接需求：返回此条用例是参考哪（几）条需求生成的，值为需求“标识”
                
                输出的测试用例内容应为中文，输出格式应当使用JSON, 每条测试用例应有如下结构:
                {{
                    "test_case_name": "<测试用例名称>",
                    "precondition": "<前置条件>",
                    "test_steps": [
                        {{
                            "step_number": <测试步骤序号>
                            "description": "<测试步骤描述>",
                            "expected_result": "<期望结果>"
                        }},
                        ...
                    ],
                    "function_module": "<功能模块>"
                    "linked_req": ["<需求“标识”>"]
                }}"""

        prompt = ChatPromptTemplate.from_template(template)

        chain = prompt | model

        response = chain.invoke({"action": f"针对以下软件需求 {requirements_text}, 为 {function_module} 功能模块生成测试用例, 并将每条测试用例链接到需求ID {', '.join(requirement_ids)}"})
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
