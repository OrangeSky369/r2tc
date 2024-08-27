# config.py

class Config:
    # 配置文件，存放与PDF解析、LLM模型等相关的配置信息
    PDF_PATH = "data/sample_document.pdf"
    MODEL_NAME = "deepseek-v2:16b"
    OUTPUT_PATH = "src/output/test_cases.json"
    REQUIRED_VALIDATION_METHOD = "HIL"
    REQUIRED_ARTIFACT_TYPE = "requirement"
