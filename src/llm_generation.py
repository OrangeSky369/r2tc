from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from prompts.file_generation_prompts import template
import json
import os


def generate_test_cases_file(model_name, aggregated_requirements):
    # Initialize Ollama model using langchian
    model = OllamaLLM(model=model_name)

    test_cases = []

    # Process each group of aggregated requirements
    for group in aggregated_requirements:
        function_module = group['function_module']
        requirements_text = "\n".join([f"- {req['主文本']}" for req in group['requirements']])
        # requirements_text = "\n".join(f"- {req['主文本']}" for req in group['requirements'])
        requirement_ids = [req['标识'] for req in group['requirements']]  # list of IDs for linked_req

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


def generate_test_cases_text(selected_llm, text_prompts):
    """
    Generate test cases using the specified LLM model.

    Arguments:
        - selected_llm: text of model name to use for generating test cases
        - template: text of prompt to use for generating test cases

    Returns:
        - text of generated test cases
    """

    model = OllamaLLM(model=selected_llm)

    prompt = ChatPromptTemplate.from_template(text_prompts)

    chain = prompt | model

    test_cases = chain.invoke({"question": "What is LangChain?"})

    return test_cases