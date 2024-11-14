#!/bin/bash

# Install dependencies from requirements.txt
pip install -r ../requirements.txt

# Reminder: Make sure you have set up your Kaggle API credentials before running this script.
# Go to your Kaggle account page.
# Under the “API” section, click “Create New API Token”. This will download a kaggle.json file containing your API credentials.
# The 'kaggle.json' file should be placed in the following directory:
# On Linux/Mac: ~/.kaggle/
# On Windows: C:\Users\<Your Username>\.kaggle\

# Run the Python pipeline script
python pipeline.py
