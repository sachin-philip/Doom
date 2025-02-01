#!/bin/bash

# Set up Python environment
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Find Python installation
PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
    osascript -e 'display dialog "Python 3 is not installed. Please install Python 3 to run this application." buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

# Directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

check_and_install_ollama() {
    if ! command -v ollama &> /dev/null; then
        osascript -e 'display dialog "Ollama is not installed. Installing now..." buttons {"OK"} default button "OK"'
        
        # Install Ollama using curl
        brew install ollama
        
        if [ $? -ne 0 ]; then
            osascript -e 'display dialog "Failed to install Ollama. Please install it manually." buttons {"OK"} default button "OK" with icon stop'
            exit 1
        fi
        
        # Wait for Ollama service to start
        sleep 3
    fi
}

# Function to check and pull Ollama model
setup_ollama_model() {
    # Check if model exists
    if ! ollama list | grep -q "deepseek-r1:1.5b"; then
        osascript -e 'display dialog "Downloading Deepseek-r1 model... This might take a few minutes." buttons {"OK"} default button "OK"'
        ollama pull deepseek-r1:1.5b
    fi
}

# Check if streamlit is installed
if ! $PYTHON_PATH -c "import streamlit" &> /dev/null; then
    osascript -e 'display dialog "Streamlit is not installed. Installing now..." buttons {"OK"} default button "OK"'
    $PYTHON_PATH -m pip install streamlit
fi

# Check if streamlit is installed
if ! $PYTHON_PATH -c "import ollama" &> /dev/null; then
    osascript -e 'display dialog "ollama sdk is not installed. Installing now..." buttons {"OK"} default button "OK"'
    $PYTHON_PATH -m pip install ollama
fi

# Check and install Ollama
check_and_install_ollama

# Setup Ollama model (only pull, don't run)
setup_ollama_model

# Launch the Streamlit app
cd "$DIR/Contents/Resources"

# Start Streamlit in the background
$PYTHON_PATH -m streamlit run main.py --server.port 8790  --server.headless true &

# Wait for the server to start (adjust sleep time if needed)
sleep 2

# Open the default browser
open http://localhost:8790

# Wait for the app process
wait