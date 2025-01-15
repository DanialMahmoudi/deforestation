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

### **1️. Data Acquisition and Exploration**
- Downloaded the deforestation dataset from the SAD Alerts and the pollution dataset from Kaggle.  
- Generated **mock data** for testing purposes to streamline CI workflows.  
- Inspected the datasets to verify formats, timestamps, and key attributes like pollutant concentrations and deforestation dates.

### **2️. Data Cleaning and Preprocessing**
- Standardized the time format and synchronized deforestation data with pollution data based on **monthly timestamps**.  
- Renamed columns to make them more intuitive (e.g., 'Date' for deforestation timestamps and pollutant columns like 'PM10', 'NO2').  
- Converted relevant columns to appropriate data types (e.g., datetime, float).  
- Handled missing values through interpolation for deforestation data. For pollutants, missing values were filled with **0**, as there were no data recording for certain pollutants.

### **3. Data Integration and Pipeline Setup** 
- Created a fully automated **ETL pipeline** (`pipeline.py`) to download, clean, and transform both datasets.  
- Integrated both deforestation and pollution data into **SQLite databases**:  
  - `deforestation.db` for deforestation alerts.  
  - `air_pollution.db` for pollution data.  
- Ensured the pipeline runs smoothly in both **local** and **GitHub Actions** environments using **mock data** for CI workflows.  
- Developed a flexible `pipeline.sh` script to control the data flow, including toggling between real and mock data.

### **4. Automated Testing (tests.sh)**
- Created a `tests.sh` script to validate the pipeline.  
- The script runs the pipeline using both **mock** and **real data** modes.  
- Checks if the `deforestation.db` and `air_pollution.db` files are generated correctly and ensures they are not empty.  
- The script automatically switches between mock and real data using an environment variable (`USE_MOCK_DATA`).

### **5. CI/CD Workflow Setup**
- Set up **GitHub Actions** for continuous integration and testing.  
- Implemented a **CI workflow** (`ci.yml`) that automatically runs the pipeline and tests on every **push to the main branch** and **pull request**.  
- The workflow uses **GitHub Secrets** to securely handle Kaggle API credentials.  
- Introduced a **workflow_dispatch** event to manually trigger the workflow and choose between **mock** and **real data** runs.  

### **6. Exploratory Data Analysis (EDA)**
- Analyzed trends for **deforestation** and each **pollutant** on a **monthly basis**.  
- Generated **line plots** to visualize the trends for deforestation and air pollutants over time.  
- Created **correlation heatmaps** to identify relationships between deforestation and various pollutants.  
- Performed **scatter plots** and **regression analyses** to check linearity and strength of correlations.

### **7. Correlation and Statistical Analysis**
- Checked for **normality** using the **Shapiro-Wilk test** and generated **Q-Q plots** for distribution analysis.  
- Calculated **Spearman's Rank Correlation** for each pollutant to measure monotonic relationships with deforestation.  
- Calculated **Kendall’s Tau** as an alternative for non-linear relationships.  

### **8. Final Report Generation**
- **analysis-report.pdf** was finalized, summarizing the key findings from trend analysis, correlation results, and interpretation.  
- **data-report.pdf** was finalized, documenting the structure, cleaning steps, and integration process for both datasets.  
- The reports include:  
  - Key insights from trend and correlation analyses.  
  - Clear answers to the main research question.  
  - Reflections on data limitations and areas for future improvement.
