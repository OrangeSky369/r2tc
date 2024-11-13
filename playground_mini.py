import gradio as gr

def my_func(a):
    return type(a), a

with gr.Blocks() as demo:
    text_genMethod = gr.CheckboxGroup(["等价类", "边界值", "故障注入"], label="用例生成方法", interactive=True)

    # 在页面上定义两个输入框，用于输入a和b的值
    input_a = gr.Text(label="a", placeholder="enter the value of a", interactive=True)
    input_b = gr.Text(label="b", placeholder="enter the value of b", interactive=True)

    # 定义一个按钮，用于触发计算a + b的结果
    calculate_button = gr.Button("Calculate!")

    # 显示成功信息或系统错误信息
    message_box_1 = gr.Textbox(label="Message", lines=2, interactive=False)
    # 显示计算a + b的结果
    message_box_2 = gr.Textbox(label="a + b", lines=1, interactive=False)
    # 显示计算a * b的结果
    message_box_3 = gr.Textbox(label="a * b", lines=1, interactive=False)

    # 定义按钮点击事件
    calculate_button.click(
        fn=my_func,
        inputs=[text_genMethod],
        outputs=[message_box_1, message_box_2]
    )


if __name__ == "__main__":
    demo.launch(share=False, server_port=7860)
