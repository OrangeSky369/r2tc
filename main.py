from src.excel_to_json import excel_to_json
from src.generate_test_cases import aggregate_requirements, generate_test_cases, save_test_cases_json
from config import Config
import json

def main():
    # Step 1: Convert requirements.xlsx to requirements.json
    # requirements_json = excel_to_json(Config.REQUIREMENTS_EXCEL_PATH, Config.REQUIREMENTS_JSON_PATH)

    with open(Config.REQUIREMENTS_JSON_PATH, 'r', encoding='utf-8') as file:
        requirements_json = json.load(file)

    aggregated_requirements = aggregate_requirements(requirements_json)
    # print(aggregated_requirements)
    str_test_cases = generate_test_cases(Config.MODEL_NAME, aggregated_requirements)
    save_test_cases_json(str_test_cases, Config.TEST_CASES_JSON_PATH)

if __name__ == '__main__':
    main()