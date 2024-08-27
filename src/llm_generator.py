# llm_generator.py
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from config import Config

class LLMGenerator:
    def __init__(self, model_name):
        self.llm = Ollama(model_name=model_name)

    def generate_test_case(self, requirement_text, requirement_id):
        prompt_template = PromptTemplate(
            input_variables=["requirement_text", "requirement_id"],
            template="""
            Given the requirement text: "{requirement_text}" with ID {requirement_id}, generate a detailed test case.
            """
        )
        prompt = prompt_template.format(requirement_text=requirement_text, requirement_id=requirement_id)
        return self.llm.generate(prompt)

    def generate_test_cases(self, requirements):
        test_cases = []
        for req_text, attributes in requirements:
            if attributes['验证方法'] == Config.REQUIRED_VALIDATION_METHOD and attributes['工件类型'] == Config.REQUIRED_ARTIFACT_TYPE:
                test_case = self.generate_test_case(req_text, attributes['标识'])
                test_cases.append(test_case)
        return test_cases
