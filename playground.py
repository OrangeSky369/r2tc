import json

def convert_string_to_json(string_content, output_file):
    # Remove the enclosing triple backticks and the `json` language identifier
    if string_content.startswith('```json'):
        string_content = string_content[7:-3].strip()

    # Parse the cleaned string content into a JSON object
    json_content = json.loads(string_content)

    # Write the JSON object to the specified output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json_content, file, ensure_ascii=False, indent=4)

# Example usage
string_input = """```json
[
    {
        "test_case_name": "TestBCM_TurnindicatorSts_OFF",
        "precondition": "CAN总线信号BCM_TurnindicatorSts为OFF",
        "test_steps": [
            {
                "step_number": 1,
                "description": "检查CAN总线信号BCM_TurnindicatorSts的值",
                "expected_result": "值为OFF"
            },
            {
                "step_number": 2,
                "description": "检查CAN总线信号ADB_TurnlndicatorReq的值是否等于CAN总线信号BCM_TurnindicatorSts",
                "expected_result": "等于OFF"
            }
        ],
        "function_module": "转向灯控制模块"
    }
]
```"""
convert_string_to_json(string_input, 'data/test_cases.json')