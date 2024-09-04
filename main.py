from src.excel_to_json import excel_to_json
from config import Config

def main():
    # Step 1: Convert requirements.xlsx to requirements.json
    requirements_json = excel_to_json(Config.EXCEL_PATH, Config.JSON_OUTPUT_PATH)

if __name__ == '__main__':
    main()