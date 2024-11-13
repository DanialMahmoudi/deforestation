# Project Plan

## Title
Deforestation and Pollution Correlation in the Amazon

## Main Question
How does deforestation in the Amazon correlate with pollution outcomes in Brazil?

## Description
Deforestation in the Amazon is a critical environmental issue, impacting both ecosystems and human health. This project aims to analyze the relationship between deforestation and pollution levels in Brazil, and more specifically, São Paulo. By correlating deforestation data with pollution indicators, we aim to uncover patterns that highlight potential public health implications and environmental changes in the region.

## Datasources

### Datasource 1: Global Forest Watch - Amazon Deforestation (SAD Alerts)
- **Metadata URL**: [Global Forest Watch SAD Alerts Data](https://data.globalforestwatch.org/datasets/gfw::sad-alerts/about)
- **Data URL**: [SAD Alerts Dataset](https://hub.arcgis.com/api/v3/datasets/9c4a16f9520447349159fa30abcea08b_2/downloads/data?format=csv&spatialRefId=3857&where=1%3D1)
- **Data Type**: Feature Layer, Custom License

The SAD Alerts dataset provides deforestation alerts specific to the Brazilian Amazon, tracking forest cover loss and degradation. This dataset allows for monitoring deforestation over time, which is crucial for identifying patterns in environmental changes.

### Datasource 2: Kaggle - Air Pollution at São Paulo, Brazil, since 2013
- **Metadata URL**: [Kaggle Data](https://www.kaggle.com/datasets/danlessa/air-pollution-at-so-paulo-brazil-since-2013)
- **Data URL**: [Kaggle Data](https://www.kaggle.com/api/v1/datasets/download/danlessa/air-pollution-at-so-paulo-brazil-since-2013)
- **Data Type**: CSV

The "Air Pollution at São Paulo, Brazil, since 2013" dataset contains historical air quality data from CETESB monitoring stations, starting in May 2013. It includes pollution index values for various pollutants categorized by air quality levels (Good, Moderate, Bad, Horrible). The dataset also provides station addresses for potential geospatial analysis.

## Work Packages

1. **Data Acquisition and Exploration**
   - Download deforestation and pollution datasets from SAD Alerts and Kaggle.
   - Inspect the datasets for data formats, timestamps, and key attributes for analysis.
  
2. **Data Cleaning and Preprocessing**
   - Standardize datasets for time and location.
   - Convert GeoTIFF and shapefiles to CSV (if necessary) to unify data formats.

3. **Data Integration and Pipeline Setup**
   - Develop a pipeline to link deforestation alerts to pollution records by region and timeframe.
   - Integrate GIS data where applicable to enhance spatial analysis.

4. **Exploratory Data Analysis (EDA)**
   - Visualize deforestation trends and pollution changes over time.
   - Identify correlations or patterns between deforestation and pollution data.

5. **Statistical Analysis**
   - Perform statistical tests to quantify the relationship between deforestation and pollution levels.
   - Evaluate temporal patterns to understand cause-effect relationships.

6. **Report Generation**
   - Summarize findings in a report, discussing the observed impact of deforestation on pollution.
   - Answer the main research question with insights and visualizations.
