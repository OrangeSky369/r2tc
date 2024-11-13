from src.excel_to_json import excel_to_json
from src.json_data_process import aggregate_requirements, save_test_cases_json
from src.llm_generation import generate_test_cases_file, generate_test_cases_text
from src.json_to_excel import json_to_excel
from prompts.text_generation_prompts import get_final_prompt
import config
import json

def run_generation_from_file():
    # Step 1: Convert requirements.xlsx to requirements.json
    excel_to_json(config.REQUIREMENTS_EXCEL_PATH, config.REQUIREMENTS_JSON_PATH)
    # requirements_json = excel_to_json(Config.REQUIREMENTS_EXCEL_PATH, Config.REQUIREMENTS_JSON_PATH)

    # Step 2: Generate test cases using LLM
    with open(config.REQUIREMENTS_JSON_PATH, 'r', encoding='utf-8') as file:
        requirements_json = json.load(file)

    aggregated_requirements = aggregate_requirements(requirements_json)
    # print(aggregated_requirements)
    str_test_cases = generate_test_cases_file(config.MODEL_NAME, aggregated_requirements)
    save_test_cases_json(str_test_cases, config.TEST_CASES_JSON_PATH)

    # Step 3: Convert test_cases.json to test_cases.xlsx
    json_to_excel(config.TEST_CASES_JSON_PATH, config.TEST_CASES_EXCEL_PATH)


def run_generation_from_text():
    # Step 1: Generate prompts (with text requirements) according to input parameters
    text_prompts = get_final_prompt(config.TEXT_REQUIREMENTS,
                                    config.SELECTED_METHODS,
                                    config.FEW_SHOTS_JSON_PATH,
                                    config.CREATIVITY_LEVEL)
    print(text_prompts)

    # Step 2: Generate text test cases using LLM
    str_test_cases = generate_test_cases_text(config.MODEL_NAME, text_prompts)
    save_test_cases_json(str_test_cases, config.TEST_CASES_JSON_PATH)

    # Step 3: Convert test_cases.json to test_cases.xlsx
    json_to_excel(config.TEST_CASES_JSON_PATH, config.TEST_CASES_EXCEL_PATH)

    return str_test_cases


