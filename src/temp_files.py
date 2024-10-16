import os
import shutil
import uuid
from datetime import datetime
import config
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


# Example usage in process_test_case_generation function
def process_test_case_generation(uploaded_file_path, selected_model):
    try:
        # Ensure the temporary sessions directory exists
        temp_sessions_dir = "temp_sessions"
        os.makedirs(temp_sessions_dir, exist_ok=True)

        # Cleanup the oldest folder if necessary
        cleanup_oldest_folder(temp_sessions_dir, max_folders=10)

        # Create a unique temporary directory for this session to avoid conflicts
        temp_dir = os.path.join(temp_sessions_dir, str(uuid.uuid4()))
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
        # run_tool()

        # Check if the output file was created successfully
        if os.path.exists(test_cases_excel_path):
            return test_cases_excel_path
        else:
            return "Error: Test cases Excel file was not created.", None

    except Exception as e:
        return f"An error occurred: {str(e)}", None

    finally:
        pass

