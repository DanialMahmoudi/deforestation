# Project Plan

## Title
Deforestation and Pollution Correlation in the Amazon

## Main Question
How does deforestation in the Amazon correlate with pollution outcomes in Brazil?

## Description
Deforestation in the Amazon is a critical environmental issue, impacting both ecosystems and human health. This project aims to analyze the relationship between deforestation and pollution levels in Brazil, specifically focusing on areas affected by Amazonian deforestation. By correlating deforestation data with pollution indicators, we aim to uncover patterns that highlight potential public health implications and environmental changes in the region.

## Datasources

### Datasource 1: Global Forest Watch - Amazon Deforestation (SAD Alerts)
- **Metadata URL**: [Global Forest Watch SAD Alerts Data](https://data.globalforestwatch.org/datasets/gfw::sad-alerts/about)
- **Data URL**: [SAD Alerts Dataset](https://data.globalforestwatch.org/datasets/gfw::sad-alerts/about)
- **Data Type**: Feature Layer, Custom License

The SAD Alerts dataset provides deforestation alerts specific to the Brazilian Amazon, tracking forest cover loss and degradation. This dataset allows for monitoring deforestation over time, which is crucial for identifying patterns in environmental changes.

### Datasource 2: OpenAQ - Air Quality Data for Brazil
- **Metadata URL**: [OpenAQ Data](https://openaq.org/#/locations)
- **Data URL**: [OpenAQ Air Quality Data](https://openaq.org/#/locations)
- **Data Type**: CSV

OpenAQ aggregates air quality data from various sources, including Brazil, and provides pollutant measurements (e.g., PM2.5, PM10). This data is useful for assessing pollution levels in areas close to deforestation sites in the Amazon, allowing for a detailed correlation analysis.

## Work Packages

1. **Data Acquisition and Exploration**
   - Download deforestation and pollution datasets from SAD Alerts and OpenAQ.
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
