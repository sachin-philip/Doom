#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install the package
pip install -e .

# Create an executable script
echo '#!/bin/bash
source "'$(pwd)'/venv/bin/activate"
streamlit run "'$(pwd)'/botter.py"' > botter
chmod +x botter

# Move the executable to a location in PATH
sudo mv botter /usr/local/bin/