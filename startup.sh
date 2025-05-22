#!/bin/bash

echo "Starting the Price Comparison Dashboard application..."

# Ensure the script exits immediately if a command exits with a non-zero status.
set -e

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Check if installation was successful (though set -e handles this)
# if [ $? -ne 0 ]; then
#     echo "Failed to install dependencies. Exiting."
#     exit 1
# fi

echo "Setting up Flask environment variables..."
export FLASK_APP=app.py
export FLASK_ENV=development # Recommended: 'production' for actual deployments

echo "Running Flask application on port 9000..."
# Using python -m flask run to ensure consistency and control over parameters
python -m flask run --host=0.0.0.0 --port=9000
