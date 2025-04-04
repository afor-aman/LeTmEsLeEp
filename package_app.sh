#!/bin/bash

# Simple script to package LetMeSleep for distribution
# This script doesn't create a standalone app but packages the Python code
# and instructions for running it

echo "Packaging LetMeSleep for distribution..."

# Create distribution directory
mkdir -p dist/LetMeSleep

# Copy Python files and resources
cp -r automation.py main.py ui dist/LetMeSleep/
cp -r resources dist/LetMeSleep/

# Create requirements.txt
cat > dist/LetMeSleep/requirements.txt << EOF
PyQt5>=5.15.0
pyautogui>=0.9.53
qdarktheme>=1.1.0
EOF

# Create a launcher script
cat > dist/LetMeSleep/run.sh << EOF
#!/bin/bash
# LetMeSleep Launcher

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 to run this application."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 to run this application."
    exit 1
fi

# Check if required packages are installed and install if needed
echo "Checking dependencies..."
pip3 install -r requirements.txt

# Launch the application
echo "Starting LetMeSleep..."
python3 main.py
EOF

# Make the launcher executable
chmod +x dist/LetMeSleep/run.sh

# Create a README file
cat > dist/LetMeSleep/README.md << EOF
# LetMeSleep

A desktop automation tool that simulates mouse movements and keyboard typing to keep your computer active.

## Requirements

- Python 3.6 or higher
- pip3

## Installation

1. Open a terminal in this directory
2. Run the launcher script:
   
   \`\`\`
   ./run.sh
   \`\`\`

   This will check for required dependencies and install them if needed.

## Features

- Mouse Automation: Move the mouse in various patterns (straight, zigzag, random)
- Keyboard Automation: Type text with randomization
- Scroll Automation: Perform random scrolling operations
- Failsafe: Move your mouse to the top-left corner (0,0) to immediately stop all automation

## Usage

Configure the settings as needed and click "Start Both" to begin automation.
EOF

# Create a ZIP file
cd dist
zip -r LetMeSleep.zip LetMeSleep

echo "Packaging complete!"
echo "Distribution package created at: $(pwd)/LetMeSleep.zip"
echo ""
echo "To use:"
echo "1. Extract the ZIP file"
echo "2. Run the 'run.sh' script to launch the application" 