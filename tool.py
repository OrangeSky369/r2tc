from src.excel_to_json import excel_to_json
from src.generate_test_cases import aggregate_requirements, generate_test_cases, save_test_cases_json
from src.json_to_excel import json_to_excel
import config
import json

def run_tool():
    # Step 1: Convert requirements.xlsx to requirements.json
    excel_to_json(config.REQUIREMENTS_EXCEL_PATH, config.REQUIREMENTS_JSON_PATH)
    # requirements_json = excel_to_json(Config.REQUIREMENTS_EXCEL_PATH, Config.REQUIREMENTS_JSON_PATH)

    # Step 2: Generate test cases using LLM
    with open(config.REQUIREMENTS_JSON_PATH, 'r', encoding='utf-8') as file:
        requirements_json = json.load(file)

    aggregated_requirements = aggregate_requirements(requirements_json)
    # print(aggregated_requirements)
    str_test_cases = generate_test_cases(config.MODEL_NAME, aggregated_requirements)
    save_test_cases_json(str_test_cases, config.TEST_CASES_JSON_PATH)

    # Step 3: Convert test_cases.json to test_cases.xlsx
    json_to_excel(config.TEST_CASES_JSON_PATH, config.TEST_CASES_EXCEL_PATH)

