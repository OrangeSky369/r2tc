import gradio as gr
import config
import os
import shutil
from datetime import datetime
import uuid

from tool import run_tool

def cleanup_oldest_folder(directory, max_folders=10):
    """
    Deletes the oldest folder in the specified directory if the number of folders exceeds max_folders.

    Args:
        directory (str): The path to the directory containing the folders.
        max_folders (int): The maximum number of folders allowed in the directory.
    """
    try:
        # List all folders in the directory
        folders = [os.path.join(directory, folder) for folder in os.listdir(directory) if
                   os.path.isdir(os.path.join(directory, folder))]

        # Sort folders by creation time
        folders.sort(key=lambda x: os.path.getctime(x))

        # Delete the oldest folder if the number of folders exceeds max_folders
        if len(folders) > max_folders:
            shutil.rmtree(folders[0])
            print(f"Deleted oldest folder: {folders[0]}")
    except Exception as e:
        print(f"An error occurred during cleanup: {str(e)}")


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
        # Ensure the temporary sessions directory exists
        temp_sessions_dir = "temp_sessions"
        os.makedirs(temp_sessions_dir, exist_ok=True)

        # Cleanup the oldest folder if necessary
        cleanup_oldest_folder(temp_sessions_dir, max_folders=10)

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
        run_tool()  # Ensure that run_tool() returns log messages as a string

        # Check if the output file was created successfully
        if os.path.exists(test_cases_excel_path):
            # Provide the path to the generated Excel file for download
            return test_cases_excel_path
        else:
            return "Error: Test cases Excel file was not created.", None

    except Exception as e:
        # Handle any unexpected errors
        return f"An error occurred: {str(e)}", None

    finally:
        # Optional: Implement cleanup logic here if needed
        pass


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