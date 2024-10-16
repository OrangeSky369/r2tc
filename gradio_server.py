import gradio as gr
import config
import os
import shutil
from datetime import datetime
import uuid

from tool import run_tool
from src.temp_files import process_test_case_generation

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Test Case Generation Tool")
    gr.Markdown("Upload your requirements Excel file, select an LLM model, and generate test cases.")

    with gr.Row():
        # File upload component
        file_input = gr.File(
            label="Upload Requirements Excel File",
            file_types=[".xlsx", ".xls"],
            type="filepath"
        )

        # Dropdown for model selection
        model_dropdown = gr.Dropdown(
            choices=config.AVAILABLE_MODELS,
            value=config.AVAILABLE_MODELS[0],
            label="Select LLM Model",
            elem_id="model_dropdown"
        )

    # Button to trigger test case generation
    generate_button = gr.Button("Generate Test Cases")

    # Text box to display messages
    message_box = gr.Textbox(
        label="Messages",
        lines=3,
        interactive=False
    )

    # Download button for the generated Excel file
    download_output = gr.File(
        label="Download Test Cases Excel"
    )

    # Define the action when the button is clicked
    generate_button.click(
        fn=process_test_case_generation,
        inputs=[file_input, model_dropdown],
        outputs=[message_box, download_output]
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
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)  # Adjust server settings as needed