import gradio as gr
import config
import os
import shutil
from datetime import datetime
import uuid

# Import your tool's main function
# Replace 'tool' and 'run_tool' with the actual module and function names if different
from tool import run_tool  # Ensure that 'tool.py' is in the same directory or properly referenced

def process_test_case_generation(uploaded_file_path, selected_model):
    """
    Processes the uploaded requirements Excel file and generates test cases.

    Args:
        uploaded_file_path (str): The file path to the uploaded Excel file containing requirements.
        selected_model (str): The selected LLM model name.

    Returns:
        tuple: A tuple containing the message log and the path to the generated Excel file.
    """
    try:
        # Create a unique temporary directory for this session to avoid conflicts
        temp_dir = os.path.join("temp_sessions", str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)

        # Define paths based on the temporary directory
        requirements_excel_path = os.path.join(temp_dir, os.path.basename(uploaded_file_path))
        requirements_json_path = os.path.join(temp_dir, "requirements.json")
        test_cases_json_path = os.path.join(temp_dir, "test_cases.json")
        test_cases_excel_path = os.path.join(temp_dir, "test_cases.xlsx")

        # Copy the uploaded Excel file to the temporary directory
        shutil.copy(uploaded_file_path, requirements_excel_path)

        # Update config.py parameters
        config.REQUIREMENTS_EXCEL_PATH = requirements_excel_path
        config.REQUIREMENTS_JSON_PATH = requirements_json_path
        config.TEST_CASES_JSON_PATH = test_cases_json_path
        config.TEST_CASES_EXCEL_PATH = test_cases_excel_path
        config.MODEL_NAME = selected_model

        # Run the test case generation tool
        messages = run_tool()  # Ensure that run_tool() returns log messages as a string

        # Check if the output file was created successfully
        if os.path.exists(test_cases_excel_path):
            # Provide the path to the generated Excel file for download
            return messages, test_cases_excel_path
        else:
            return "Error: Test cases Excel file was not created.", None

    except Exception as e:
        # Handle any unexpected errors
        return f"An error occurred: {str(e)}", None

    finally:
        # Optional: Implement cleanup logic here if needed
        # For example, you can schedule deletion of old temp directories
        pass

# Define the available LLM models
AVAILABLE_MODELS = [
    "glm4:latest",
    "qwen2:latest",
    "deepseek-v2:16b",
    "gemma2:9b",
    "llama3.1:latest",
    "mistral:latest"
]

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Test Case Generation Tool")
    gr.Markdown("Upload your requirements Excel file, select an LLM model, and generate test cases.")

    with gr.Row():
        # File upload component
        file_input = gr.File(
            label="Upload Requirements Excel File",
            file_types=[".xlsx", ".xls"],
            type="filepath"  # Changed from "file" to "filepath"
        )

        # Dropdown for model selection
        model_dropdown = gr.Dropdown(
            choices=AVAILABLE_MODELS,
            value=AVAILABLE_MODELS[0],
            label="Select LLM Model"
        )

    # Button to trigger test case generation
    generate_button = gr.Button("Generate Test Cases")

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

    # Define the action when the button is clicked
    generate_button.click(
        fn=process_test_case_generation,
        inputs=[file_input, model_dropdown],
        outputs=[message_box, download_output]
    )

    # Optional: Add some styling or additional information
    gr.Markdown("""
    ---
    **Note:** Ensure that the uploaded Excel file follows the required format. If you encounter any issues, please check the messages above for more details.
    """)

# Launch the Gradio interface
if __name__ == "__main__":
    # Ensure the temporary sessions directory exists
    os.makedirs("temp_sessions", exist_ok=True)
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)  # Adjust server settings as needed