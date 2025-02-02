#!/bin/bash

# Create virtual environment
python3 -m venv venv1
source venv1/bin/activate

# Install required packages
pip install py2app
pip install streamlit
# Add other dependencies your app needs
pip install --upgrade pip  # Ensure latest pip
pip install PyInstaller  # Add PyInstaller explicitly
pip install -r requirements.txt

# Clean build directories
rm -rf build dist

# Build the app
python setup.py py2app --no-strip

# Create run script
cat > dist/DoomChat.app/Contents/MacOS/run_streamlit.sh << 'EOF'
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PATH="$DIR:$PATH"
cd "$DIR"
./streamlit_app run "$DIR/../Resources/main.py"
EOF

chmod +x dist/DoomChat.app/Contents/MacOS/run_streamlit.sh

echo "Build complete! App is in the dist directory."