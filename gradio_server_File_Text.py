import gradio as gr
import config
import os

from src.temp_files import process_test_case_generation_file, process_test_case_generation_text
# from playground import message_box_test

def change_para(choice):
    # 事件侦听器函数的返回值通常是相应输出组件的更新值。
    # 有时我们也希望更新组件的配置，例如可见性。
    # 在本例中，我们返回一个对象，而不仅仅是更新组件值。
    if choice == "默认":
        return gr.update(visible=False)
    elif choice == "自定义":
        return gr.update(visible=True)
    
# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Test Case Generation Tool")
    gr.Markdown("Upload your requirements Excel file, select an LLM model, and generate test cases.")                    

    with gr.Tabs():
        with gr.TabItem("文件模态"):
            with gr.Row():
                with gr.Column():
                    # File upload component
                    file_input = gr.File(
                        label="Upload Requirements Excel File",
                        #file_types=[".xlsx", ".xls"],
                        type="filepath"
                    )
                    # Dropdown for model selection
                    model_dropdown = gr.Dropdown(
                        choices=config.AVAILABLE_MODELS,
                        value=config.AVAILABLE_MODELS[0],
                        label="Select LLM Model",
                        elem_id="model_dropdown",
                        interactive=True
                    )
                    # 通过以下几行 控制 model_genpara 等组件的是否显示
                    radio = gr.Radio(["默认", "自定义"], label="用例生成参数", value="默认")
                    # select test case generation method
                    model_genpara = gr.Radio(["忠实内容", "放飞自我"], label="模型参数",value="忠实内容",visible=False,interactive=True)
                    # 
                    testcase_genMethod = gr.CheckboxGroup(["等价类", "边界值", "故障注入"], label="用例生成方法",visible=False,interactive=True)

                    radio.change(fn=change_para, inputs=radio, outputs=model_genpara)
                    radio.change(fn=change_para, inputs=radio, outputs=testcase_genMethod)

                    # Button to trigger test case generation
                    generate_button = gr.Button("Generate Test Cases")            
                with gr.Column():    
                    # Text box to display messages
                    message_box = gr.Textbox(
                        label="Messages",
                        lines=10,
                        interactive=False
                    )   
                    # Download button for the generated Excel file
                    download_output = gr.File(
                        label="Download Test Cases Excel"
                    )
            if radio.value == "默认":        
                generate_button.click(
                    # fn=message_box_test,
                    fn=process_test_case_generation_file,
                    inputs=[file_input, model_dropdown],
                    outputs=[message_box, download_output]
                )
            elif radio.value == "自定义":
                generate_button.click(
                    # fn=message_box_test,
                    fn=process_test_case_generation_text,
                    inputs=[file_input, model_dropdown],#, model_genpara, testcase_genMethod],#增加函数接口参数
                    outputs=[message_box, download_output]
                )
        with gr.TabItem("文本模态"):
            with gr.Row():
                with gr.Column():                        
                    text_reqID = gr.Text(label="需求ID", placeholder="请输入需求ID", interactive=True)
                    text_req   = gr.Text(label="需求内容", lines=3, placeholder="请输入需求内容", interactive=True)
                    # Dropdown for model selection
                    text_dropdown = gr.Dropdown(
                        choices=config.AVAILABLE_MODELS,
                        value=config.AVAILABLE_MODELS[0],
                        label="Select LLM Model",
                        elem_id="model_dropdown",
                        interactive=True
                    )
                    # 通过以下几行 控制 model_genpara 等组件的是否显示
                    text_radio = gr.Radio(["默认", "自定义"], label="用例生成参数", value="默认")
                    # select test case generation method
                    text_genpara = gr.Radio(["忠实内容", "放飞自我"], label="模型参数",value="忠实内容",visible=False,interactive=True)
                    # 
                    text_genMethod = gr.CheckboxGroup(["等价类", "边界值", "故障注入"], label="用例生成方法",visible=False,interactive=True)

                    text_radio.change(fn=change_para, inputs=text_radio, outputs=text_genpara)
                    text_radio.change(fn=change_para, inputs=text_radio, outputs=text_genMethod)

                    # Button to trigger test case generation
                    text_button = gr.Button("Generate Test Cases")            
                with gr.Column():    
                    # Text box to display messages
                    text_box = gr.Textbox(
                        label="Messages",
                        lines=6,
                        interactive=False
                    )
                    # output test case
                    text_output1 = gr.Textbox(label="生成内容", lines=6, placeholder="生成测试用例")   
                    # Download button for the generated Excel file
                    text_output = gr.File(
                        label="Download Test Cases Excel"
                    )
            generate_button.click(
                # fn=message_box_test,
                fn=process_test_case_generation_text,
                inputs=[text_req, text_genMethod, text_genpara, text_dropdown],#需要修改相应的函数输入接口内容
                outputs=[text_box, text_output1, text_output]
            )

    # Optional: Add some styling or additional information
    gr.Markdown("""
    ---
    **Note:** The uploaded Excel file follows the format of EML. If you encounter any issues, please check the messages above for more details.
    """)

# Launch the Gradio interface
if __name__ == "__main__":
    # Ensure the temporary sessions directory exists
    os.makedirs("temp_sessions", exist_ok=True)
    demo.launch(share=True)#share=False, server_name="0.0.0.0", server_port=7860)  # Adjust server settings as needed
