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

# Check if streamlit is installed
if ! $PYTHON_PATH -c "import streamlit" &> /dev/null; then
    osascript -e 'display dialog "Streamlit is not installed. Installing now..." buttons {"OK"} default button "OK"'
    $PYTHON_PATH -m pip install streamlit
fi

# Launch the Streamlit app
cd "$DIR/Contents/Resources"

# Start Streamlit in the background
$PYTHON_PATH -m streamlit run app.py --server.port 8790  --server.headless true &

# Wait for the server to start (adjust sleep time if needed)
sleep 2

# Open the default browser
open http://localhost:8790

# Wait for the app process
wait