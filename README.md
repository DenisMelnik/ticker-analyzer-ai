# Ticker Analyser

## Overview
A multi-agent AI assistant for analyzing stock tickers using CrewAI. It validates tickers, analyzes price data and news sentiment, and provides a final recommendation (Buy/Sell/Hold) with explanations.

## Project Structure
- `src/` - Source code
  - `agents/` - CrewAI agent definitions
  - `utils/` - Utilities and helpers
  - `controller.py` - Main workflow orchestrator
- `unit_tests/` - Pytest test cases
  - `agents/` - Tests for agent implementations
  - `utils/` - Tests for utility functions

## Requirements
- Python 3.11 or higher
- API Keys:
  - OpenAI API key
  - Brave Search API key

## Setup

### Automatic Setup (Recommended)
Run the setup script:

```sh
# Make the script executable first
chmod +x setup.sh
./setup.sh
```

The script will:
1. Check if Python is installed and verify its version (3.11+)
2. Create a virtual environment
3. Install dependencies from requirements.txt
4. Create a .env file for your API keys
5. Provide activation instructions

### Manual Setup
If you prefer to set up manually:

1. **Check Python version:**
   Make sure you have Python 3.11+ installed:
   ```sh
   python --version
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   
   # Activate the virtual environment
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   BRAVE_API_KEY=your_brave_api_key_here
   ```

## Usage
After activating your virtual environment:

```sh
python src/controller.py
```

You'll be prompted to enter a stock ticker symbol (e.g., AAPL, MSFT) for analysis. 

### Features
- **Multiple Ticker Analysis**: After completing one analysis, you'll be prompted to enter another ticker or exit
- **Comprehensive Analysis**: Combines price data, news, sentiment analysis, and investment recommendations
- **Validation**: Ensures ticker symbols are valid before proceeding with analysis

### Sample Flow
```
Enter a stock ticker symbol (e.g., AAPL) or 'quit' to exit: AAPL
[Analysis results shown here]
--------------------------------------------------------------------------------
Analysis for AAPL completed.
--------------------------------------------------------------------------------

Enter a stock ticker symbol (e.g., AAPL) or 'quit' to exit: MSFT
[Analysis results shown here]
--------------------------------------------------------------------------------
Analysis for MSFT completed.
--------------------------------------------------------------------------------

Enter a stock ticker symbol (e.g., AAPL) or 'quit' to exit: quit
Thank you for using CrewAI Ticker Analysis Assistant. Goodbye!
```

## Code Quality
- The project uses Ruff for linting and enforces the following rules:
  - PEP 8 style guide compliance (E)
  - Pyflakes logical errors (F)
  - Import sorting (I)
  - Bugbear common bugs detection (B)
  - Modern Python syntax (UP)

- We provide a comprehensive quality check script:
  ```sh
  ./quality_check.sh  # Runs code style checks and tests in one command
  ```
  This script:
  - Runs Ruff to check and fix code style issues
  - Executes all tests to ensure functionality works
  - Provides a single pass/fail result for quick verification

- For manual code quality checks:
  ```sh
  python -m ruff check .  # Check the entire codebase
  python -m ruff check . --fix  # Auto-fix issues where possible
  ```

## Testing
- Run all tests:
  ```sh
  pytest
  ```

- Run tests with coverage report:
  ```sh
  pytest --cov=src
  ```

- Generate HTML coverage report:
  ```sh
  pytest --cov=src --cov-report=html
  ```
  
- Run specific test modules:
  ```sh
  pytest unit_tests/agents/  # Run only agent tests
  pytest unit_tests/utils/   # Run only utility tests
  ```

## Troubleshooting
- **Python Version Issues**: If you don't have Python 3.11+, consider using a Python version manager like pyenv to install and manage multiple versions.
- **API Key Issues**: Make sure your API keys are correctly set in the `.env` file.
- **Installation Issues**: If you encounter issues installing packages, try upgrading pip: `pip install --upgrade pip`

## License
MIT
