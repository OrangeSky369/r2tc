# main.py
from config import Config
from document_parser import DocumentParser
from llm_generator import LLMGenerator
from utils import save_test_cases

def main():
    # 第一步：解析文档，提取需求和属性
    parser = DocumentParser(Config.PDF_PATH)
    requirements = parser.extract_requirements()

    # 第二步：使用LLM生成测试用例
    generator = LLMGenerator(Config.MODEL_NAME)
    test_cases = generator.generate_test_cases(requirements)

    # 第三步：保存生成的测试用例
    save_test_cases(test_cases, Config.OUTPUT_PATH)
    print(f"Test cases generated and saved to {Config.OUTPUT_PATH}")

if __name__ == "__main__":
    main()
