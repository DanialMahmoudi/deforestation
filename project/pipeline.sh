#!/bin/bash

# Change to the directory where this script is located (pipeline.sh)
cd "$(dirname "$0")"

# Set paths to the correct relative locations
REQUIREMENTS="../requirements.txt"  # Adjusted path for requirements.txt
PIPELINE_PY="./pipeline.py"  # No change needed for pipeline.py, since it's in the same folder
DATA_DIR="../data"  # Adjusted path for data directory

# Check if requirements.txt exists
if [ ! -f "$REQUIREMENTS" ]; then
    echo "❌ requirements.txt not found."
    exit 1
fi

# Install dependencies from requirements.txt
pip install -r "$REQUIREMENTS"

# Reminder: Make sure you have set up your Kaggle API credentials before running this script.
# Go to your Kaggle account page.
# Under the “API” section, click “Create New API Token”. This will download a kaggle.json file containing your API credentials.
# The 'kaggle.json' file should be placed in the following directory:
# On Linux/Mac: ~/.kaggle/
# On Windows: C:\Users\<Your Username>\.kaggle\

# Check if pipeline.py exists
if [ ! -f "$PIPELINE_PY" ]; then
    echo "❌ pipeline.py not found."
    exit 1
fi

# Run the Python pipeline script
python "$PIPELINE_PY"
