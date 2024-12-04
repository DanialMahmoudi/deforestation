#!/bin/bash

# Execute the script from project directory
cd "$(dirname "$0")"

# Set relative paths
PIPELINE="./pipeline.sh"
DATA_DIR="../data"
DEFORESTATION_DB="$DATA_DIR/deforestation.db"
AIR_POLLUTION_DB="$DATA_DIR/air_pollution.db"

# Run the pipeline
echo "Running the pipeline script..."
bash "$PIPELINE"

# Check if deforestation.db exists
if [ -f "$DEFORESTATION_DB" ]; then
    echo "✅ $DEFORESTATION_DB exists."
else
    echo "❌ $DEFORESTATION_DB is missing."
    exit 1
fi

# Check if air_pollution.db exists
if [ -f "$AIR_POLLUTION_DB" ]; then
    echo "✅ $AIR_POLLUTION_DB exists."
else
    echo "❌ $AIR_POLLUTION_DB is missing."
    exit 1
fi

# Ensure deforestation.db is not empty
if [ -s "$DEFORESTATION_DB" ]; then
    echo "✅ $DEFORESTATION_DB is not empty."
else
    echo "❌ $DEFORESTATION_DB is empty."
    exit 1
fi

# Ensure air_pollution.db is not empty
if [ -s "$AIR_POLLUTION_DB" ]; then
    echo "✅ $AIR_POLLUTION_DB is not empty."
else
    echo "❌ $AIR_POLLUTION_DB is empty."
    exit 1
fi

echo "✅ All tests passed successfully!"
exit 0
