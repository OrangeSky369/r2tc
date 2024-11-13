REQUIREMENTS_EXCEL_PATH = './data/requirements.xlsx'
REQUIREMENTS_JSON_PATH = './data/requirements.json'
TEST_CASES_JSON_PATH = './data/test_cases.json'
TEST_CASES_EXCEL_PATH = './data/test_cases.xlsx'

MODEL_NAME = "glm4:latest"

# Define the available LLM models
AVAILABLE_MODELS = [
    "glm4:latest",
    "qwen2:latest",
    "deepseek-v2:16b",
    "gemma2:9b",
    "llama3.1:latest",
    "mistral:latest"
]

TEXT_REQUIREMENTS = ""

SELECTED_METHODS = []

CREATIVITY_LEVEL = ""

FEW_SHOTS_JSON_PATH = './prompts/few_shots.json'