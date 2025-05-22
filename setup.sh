#!/bin/bash

set -e

# Colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up CrewAI Ticker Analysis Assistant...${NC}\n"

# Check if Python is installed
check_python() {
    echo "Checking for Python installation..."
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}Python is not installed or not in your PATH.${NC}"
        echo -e "${YELLOW}Please install Python 3.11 or higher before continuing.${NC}"
        echo "Visit https://www.python.org/downloads/ for installation instructions."
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print('{}.{}'.format(sys.version_info.major, sys.version_info.minor))")
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    echo "Found Python $PYTHON_VERSION"
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
        echo -e "${RED}Error: Python 3.11 or higher is required.${NC}"
        echo -e "${YELLOW}Consider using pyenv to install and manage Python versions:${NC}"
        echo "https://github.com/pyenv/pyenv"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Python version check passed.${NC}"
}

# Create virtual environment
create_venv() {
    echo "Setting up virtual environment..."
    
    # Check if venv directory exists but is incomplete/corrupted
    if [ -d "venv" ]; then
        if [ ! -f "venv/bin/pip" ] || [ ! -f "venv/bin/python" ]; then
            echo -e "${YELLOW}Found existing but incomplete virtual environment. Removing it...${NC}"
            rm -rf venv
            echo "Recreating virtual environment..."
            $PYTHON_CMD -m venv venv
            if [ $? -ne 0 ]; then
                echo -e "${RED}Failed to create virtual environment.${NC}"
                exit 1
            fi
        else
            echo "Virtual environment already exists."
        fi
    else
        echo "Creating new virtual environment..."
        $PYTHON_CMD -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create virtual environment.${NC}"
            exit 1
        fi
    fi
    
    # Verify virtual environment
    if [ -f "venv/bin/python" ] && [ -f "venv/bin/pip" ]; then
        echo -e "${GREEN}✓ Virtual environment is ready.${NC}"
    else
        echo -e "${RED}Error: Virtual environment setup failed.${NC}"
        exit 1
    fi
}

# Install requirements
install_requirements() {
    echo "Installing requirements..."
    ./venv/bin/pip install --upgrade pip
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to upgrade pip.${NC}"
        exit 1
    fi
    
    ./venv/bin/pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install requirements.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Dependencies installed.${NC}"
}

# Create environment file
create_env_file() {
    echo "Checking for environment file..."
    if [ -f ".env" ]; then
        echo ".env file already exists."
    elif [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file from .env.example${NC}"
        echo -e "${YELLOW}Please edit the .env file with your actual API keys.${NC}"
    else
        cat > .env << EOF
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
BRAVE_API_KEY=your_brave_api_key_here

# Other configuration options
DEBUG=false
EOF
        echo -e "${GREEN}✓ Created default .env file.${NC}"
        echo -e "${YELLOW}Please edit the .env file with your actual API keys.${NC}"
    fi
}

# Run all setup steps
check_python
create_venv
install_requirements
create_env_file

# Done!
echo -e "\n${GREEN}Setup completed successfully!${NC}"
echo -e "\nTo activate the virtual environment, run:"
echo -e "${YELLOW}source venv/bin/activate${NC}"
echo -e "\nAfter activation, you can run the application with:"
echo -e "${YELLOW}python src/controller.py${NC}" 