template = """
Action: {action}

以下是测试用例生成要求：

为需求中"验证方法Verification Method"参数为"HIL"，且"工件类型"参数为"Requirement"的需求生成测试用例。每条测试用例应包含：
- 一个描述性的用例名称
- 前置条件
- 若干测试步骤，每个测试步骤都包含描述和预期结果
- 功能模块
- 链接需求：返回此条用例是参考哪（几）条需求生成的，值为需求“标识”

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
}}"""