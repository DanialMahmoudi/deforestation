#!/bin/bash

# Execute the script from project directory
cd "$(dirname "$0")"

# Set relative paths
PIPELINE="./pipeline.sh"
DATA_DIR="../data"
DEFORESTATION_DB="$DATA_DIR/deforestation.db"
AIR_POLLUTION_DB="$DATA_DIR/air_pollution.db"

# Run pipeline with mock data
echo "Running pipeline with mock data..."
USE_MOCK_DATA=true bash "$PIPELINE"

# Check if deforestation.db exists
if [ -f "$DEFORESTATION_DB" ]; then
    echo "✅ Mock deforestation.db exists."
else
    echo "❌ Mock deforestation.db is missing."
    exit 1
fi

# Check if air_pollution.db exists
if [ -f "$AIR_POLLUTION_DB" ]; then
    echo "✅ Mock air_pollution.db exists."
else
    echo "❌ Mock air_pollution.db is missing."
    exit 1
fi

# Ensure deforestation.db is not empty
if [ -s "$DEFORESTATION_DB" ]; then
    echo "✅ Mock $DEFORESTATION_DB is not empty."
else
    echo "❌ Mock $DEFORESTATION_DB is empty."
    exit 1
fi

# Ensure air_pollution.db is not empty
if [ -s "$AIR_POLLUTION_DB" ]; then
    echo "✅ Mock $AIR_POLLUTION_DB is not empty."
else
    echo "❌ Mock $AIR_POLLUTION_DB is empty."
    exit 1
fi

# Run the pipeline with real data
echo "Running the pipeline script with real data..."
USE_MOCK_DATA=false bash "$PIPELINE"

# Check if deforestation.db exists
if [ -f "$DEFORESTATION_DB" ]; then
    echo "✅ Real $DEFORESTATION_DB exists."
else
    echo "❌ Real $DEFORESTATION_DB is missing."
    exit 1
fi

# Check if air_pollution.db exists
if [ -f "$AIR_POLLUTION_DB" ]; then
    echo "✅ Real $AIR_POLLUTION_DB exists."
else
    echo "❌ Real $AIR_POLLUTION_DB is missing."
    exit 1
fi

# Ensure deforestation.db is not empty
if [ -s "$DEFORESTATION_DB" ]; then
    echo "✅ Real $DEFORESTATION_DB is not empty."
else
    echo "❌ Real $DEFORESTATION_DB is empty."
    exit 1
fi

# Ensure air_pollution.db is not empty
if [ -s "$AIR_POLLUTION_DB" ]; then
    echo "✅ Real $AIR_POLLUTION_DB is not empty."
else
    echo "❌ Real $AIR_POLLUTION_DB is empty."
    exit 1
fi

echo "✅ All tests passed successfully!"
exit 0
