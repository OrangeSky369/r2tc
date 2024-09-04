import pandas as pd
import json

def excel_to_json(excel_path, json_output_path):
    # Read the excel file
    df = pd.read_excel(excel_path, dtype=str) # Read all columns as strings

    # Remove rows after the first empty row
    df = df.loc[:df.isnull().all(axis=1).idxmax() - 1]

    # Convert '主文本' column to properly handle double quotes
    df['主文本'] = df['主文本'].apply(lambda x: x.replace('\\"', '"').replace('"', ''))

    # Convert the dataframe to a json
    requirements_json = df.to_dict(orient='records')

    # Save json data to file
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(requirements_json, json_file, ensure_ascii=False, indent=4)

    print(f"Converted requirements Excel file to JSON file: {json_output_path}")
    return requirements_json
