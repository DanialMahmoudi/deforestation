# Project Plan

## Title
**Deforestation and Pollution Correlation in the Amazon**

## Main Question
How does deforestation in the Amazon correlate with pollution outcomes in Brazil?

## Description
This project investigates the environmental and public health implications of deforestation in the Amazon by correlating it with pollution data from São Paulo, Brazil. By combining deforestation alerts with air quality measures, we aim to uncover patterns that highlight potential environmental changes and public health risks.

## Datasources

### Datasource 1: Global Forest Watch - Amazon Deforestation (SAD Alerts)
- **Metadata URL**: [Global Forest Watch SAD Alerts Data](https://data.globalforestwatch.org/datasets/gfw::sad-alerts/about)
- **Data URL**: [SAD Alerts Dataset](https://hub.arcgis.com/api/v3/datasets/9c4a16f9520447349159fa30abcea08b_2/downloads/data?format=csv&spatialRefId=3857&where=1%3D1)
- **Data Type**: CSV (Feature Layer, Custom License)

This dataset provides deforestation alerts from the Brazilian Amazon, helping to monitor forest loss and degradation over time. These alerts will be analyzed for patterns of deforestation in relation to air pollution.

### Datasource 2: Kaggle - Air Pollution at São Paulo, Brazil, since 2013
- **Metadata URL**: [Kaggle Data](https://www.kaggle.com/datasets/danlessa/air-pollution-at-so-paulo-brazil-since-2013)
- **Data URL**: [Kaggle Data](https://www.kaggle.com/api/v1/datasets/download/danlessa/air-pollution-at-so-paulo-brazil-since-2013)
- **Data Type**: CSV

This dataset contains historical air quality data from CETESB monitoring stations in São Paulo, Brazil. The pollution data covers various pollutants and air quality levels, providing insights into pollution trends in the region.

## Work Packages

### 1. Data Acquisition and Exploration
   - Download the deforestation dataset from the SAD Alerts and the pollution dataset from Kaggle.
   - Inspect the datasets to verify formats, timestamps, and key attributes like pollutant concentrations and deforestation dates.

### 2. Data Cleaning and Preprocessing
   - Standardize the time format and synchronize deforestation data with pollution data based on timestamps and locations.
   - Rename columns to make them more intuitive, e.g., 'Date' for deforestation timestamps and 'Time' for pollution timestamps.
   - Convert relevant columns to appropriate data types (e.g., datetime, float).
   - Handle missing or invalid values (e.g., dropping rows with missing critical data).

### 3. Data Integration and Pipeline Setup
   - Create an ETL pipeline to download, clean, and transform the data.
   - Integrate both deforestation and pollution data into SQLite databases, making them ready for analysis.
   - Ensure the pipeline works on both local and supervisor environments by testing with `pipeline.sh`.
