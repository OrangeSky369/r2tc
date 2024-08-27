# Requirements to Test Cases

This project automates the generation of test cases from requirements documents using a large language model (LLM) managed by Ollama and integrated with LangChain.

## Project Structure

- `data/`: Contains sample documents.
- `src/`: Contains the main code.
  - `config.py`: Configuration settings.
  - `document_parser.py`: Parses the PDF document to extract requirements.
  - `llm_generator.py`: Uses LLM to generate test cases.
  - `utils.py`: Utility functions for saving and loading test cases.
  - `output/`: Stores generated test cases.
- `tests/`: Contains unit tests.
- `requirements.txt`: Python dependencies.

## Getting Started

1. Place your PDF document in the `data/` directory.
2. Update the `config.py` file with the appropriate settings.
3. Run `main.py` to generate test cases.

## Requirements

- Python 3.x
- Required Python packages can be installed via `pip install -r requirements.txt`.
