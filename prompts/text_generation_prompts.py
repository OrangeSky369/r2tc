import json


def get_methods_prompt(selected_methods):
    """
    Create a prompt for generation methods.
    :param selected_methods: list of selected methods for generating test cases
    :return text of the prompt
    """

    methods_prompt = "、".join(selected_methods)

    return methods_prompt


def get_creativity_level_prompt(creativity_level):
    """
    Create a prompt for creativity level.
    :param creativity_level:integer indicating the creativity level
    :return text of the prompt
    """

    if creativity_level == "忠实内容":
        creativity_instruction = "生成内容须严格遵循需求文本，用例的测试范围不应超出需求内容。"
    else:
        creativity_instruction = "生成测试用例时应高度发挥想象。"

    return creativity_instruction


def load_few_shots(filepath):
    """
    Load few shots from a JSON file.
    :param filepath: path to the JSON file
    :return dict_few_shots: few shots in dictionary format
    """

    with open(filepath, "r", encoding="utf-8") as f:
        dict_few_shots = json.load(f)

    return dict_few_shots


def get_few_shots_prompt(selected_methods, dict_few_shots):
    """
    :param selected_methods: list of selected_methods
    :param dict_few_shots:
    :return text of few shots prompt for all the generation methods
    """

    few_shots_prompt = ""

    for method in selected_methods:
        if method in dict_few_shots:
            few_shots_prompt += f"{method}方法：\n"
            examples = dict_few_shots[method]
            for example in examples:
                few_shots_prompt += f"需求：\n{example['example_name']}\n"
                few_shots_prompt += f"测试用例：\n{example['example_description']}\n\n"

    return few_shots_prompt


def get_final_prompt(requirements, selected_methods, few_shots_json_filepath, creativity_level):
    """
    Create a prompt for generating test cases, combining with different input parameters.
    :param requirements: text of input requirements to generate test cases
    :param selected_methods: list of methods name to generate test cases
    :param few_shots_json_filepath: filepath of the json file, which contains examples of each generation method
    :param creativity_level: text of description indicating the creativity level
    :return final_prompt: text of the final prompt
    """

    # get each part of the prompt
    methods_prompt = get_methods_prompt(selected_methods)
    dict_few_shots = load_few_shots(few_shots_json_filepath)
    few_shots_prompt = get_few_shots_prompt(selected_methods, dict_few_shots)
    creativity_level_prompt = get_creativity_level_prompt(creativity_level)

    final_prompt = f"""
根据以下需求生成测试用例：
{requirements}

输出的测试用例内容应为中文，输出格式应当使用JSON, 每条测试用例应有如下结构:
{{
    "test_case_name": "<测试用例名称>",
    "precondition": "<前置条件>",
    "test_steps": [
        {{
            "step_number": <测试步骤序号>
            "description": "<测试步骤描述>",
            "expected_result": "<期望结果>"
        }},
        ...
    ],
    "function_module": "<功能模块>"
    "linked_req": ["<需求“标识”>"]
}}

测试用例生成要求：
生成的测试用例中"linked_req"字段暂时不填写。
可以由一条需求文本生成多条测试用例，也可以由一条需求文本生成一条测试用例。
一条测试用例可以有超过一个验证项。
一条测试用例可以包含多个测试步骤。

当需求文本中包含优先级内容时，测试用例的设计需包含以下内容：
先激活低优先级功能，再激活高优先级功能，此时系统应为高优先级功能的状态；
系统复位后，先激活高优先级功能，再激活低优先级功能，此时系统应仍保持高优先级功能的状态。

使用以下方法：{methods_prompt}生成测试用例。

举例说明：
{few_shots_prompt}

生成用例的创造性程度：{creativity_level_prompt}
"""

    return final_prompt


