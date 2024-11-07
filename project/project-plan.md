# Project Plan

## Title
Deforestation and Pollution in the Amazon: Analyzing the Correlation in Brazil

## Main Question
How does deforestation in the Amazon correlate with pollution outcomes in Brazil?

## Description
Deforestation in the Amazon is a significant environmental issue with potential consequences for air quality and public health. This project will analyze the correlation between deforestation rates in the Amazon and pollution outcomes in Brazil, focusing on the impact of forest loss on air pollution metrics such as particulate matter (PM2.5) and CO2 levels. By analyzing this relationship, the project aims to provide insights into the environmental and health implications of deforestation, helping to inform policy decisions and conservation efforts.

## Datasources

### Datasource 1: Global Forest Watch - Amazon Deforestation
- **Metadata URL**: [Global Forest Watch Data](https://data.globalforestwatch.org/)
- **Data URL**: [Amazon Deforestation Data](https://data.globalforestwatch.org/datasets/prodes-deforestation-in-brazil-legal-amazon)
- **Data Type**: CSV, GeoTIFF, Shapefiles

Global Forest Watch provides comprehensive datasets on deforestation, specifically in the Amazon. The PRODES dataset tracks deforestation in Brazil’s Amazon region, offering insights into forest cover loss over time.

### Datasource 2: OpenAQ - Air Quality Data for Brazil
- **Metadata URL**: [OpenAQ Data](https://openaq.org/#/locations)
- **Data URL**: [OpenAQ Air Quality Data](https://openaq.org/#/locations)
- **Data Type**: CSV

OpenAQ aggregates air quality data from a variety of sources, including Brazil. It provides pollutant measurements such as PM2.5, PM10, and CO2 levels, which are useful for analyzing the relationship between deforestation and pollution in Brazilian cities, especially those near the Amazon region.

### Datasource 3: INMET - Brazilian Air Quality Monitoring Network
- **Metadata URL**: [INMET Air Quality](http://www.inmet.gov.br/portal/)
- **Data URL**: [INMET Air Quality Data](http://www.inmet.gov.br/portal/)
- **Data Type**: CSV, Excel

The Brazilian National Institute of Meteorology (INMET) offers air quality data for several cities in Brazil, including regions near the Amazon. This data includes pollutants such as ozone, PM10, and CO2, which can be analyzed in relation to deforestation trends.

## Work Packages

### 1. Dataset Collection and Integration
- **Objective**: Collect the required datasets (deforestation and air quality), ensuring they are publicly available and licensed under open data licenses.
- **Tasks**:
  - Download Sentinel-2 satellite images (GeoTIFF).
  - Download air quality data for Brazil (CSV).
  - Integrate both datasets into a unified structure suitable for analysis.
- **Tools**: Python (pandas, geopandas), Data APIs (if applicable).

### 2. Data Preprocessing
- **Objective**: Clean the data, handle missing values, and transform it into a usable format for analysis.
- **Tasks**:
  - Clean the air quality data (remove duplicates, fill missing values, etc.).
  - Process the GeoTIFF images (convert to CSV or extract relevant features like pixel values and coordinates).
  - Handle missing or inconsistent data points in both datasets.
- **Tools**: Python (pandas, numpy, geopandas), Rasterio for GeoTIFF handling.

### 3. Data Transformation and Feature Engineering
- **Objective**: Convert spatial data into tabular form and create meaningful features for analysis.
- **Tasks**:
  - For deforestation data: Extract pixel values and create relevant time-series data for each region.
  - For air quality data: Derive time-series data for pollutants over time.
  - Merge the datasets based on time and region for a unified analysis.
- **Tools**: Python (pandas, numpy, geopandas).

### 4. Correlation Analysis and Exploratory Data Analysis (EDA)
- **Objective**: Analyze and visualize the correlation between deforestation and pollution.
- **Tasks**:
  - Calculate correlations (Pearson, Spearman) between deforestation trends and pollution levels.
  - Visualize the relationships between the datasets using heatmaps, scatter plots, and time-series analysis.
- **Tools**: Python (matplotlib, seaborn, pandas), Jupyter Notebooks.

### 5. Data Pipeline Creation
- **Objective**: Develop a data pipeline that automates the process of collecting, preprocessing, and analyzing the data.
- **Tasks**:
  - Build scripts to automate dataset downloading and processing.
  - Set up periodic data updates using scheduled jobs or Airflow.
  - Create a modular pipeline that can be easily adapted for future use.
- **Tools**: Python (Airflow, pandas), API Integration (if needed).

### 6. Reporting and Documentation
- **Objective**: Summarize the methodology, data, and findings in a report.
- **Tasks**:
  - Write a detailed report describing the dataset, the methods used, and the analysis results.
  - Document the pipeline and code used to process and analyze the data.
- **Tools**: Jupyter Notebooks, Markdown.

