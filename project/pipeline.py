import os
import sqlite3
import requests
import subprocess
import pandas as pd
import sys
import time
from functools import wraps


# Detect virtual environment path dynamically
venv_path = os.path.join(sys.prefix, 'Scripts', 'kaggle.exe') if os.name == 'nt' else os.path.join(sys.prefix, 'bin', 'kaggle')

# Set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(script_dir, '..', 'data'))
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

deforestation_url = "https://hub.arcgis.com/api/v3/datasets/9c4a16f9520447349159fa30abcea08b_2/downloads/data?format=csv&spatialRefId=3857&where=1%3D1"

# Retry decorator
def retry_on_failure(retries=100, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}. Retrying in {delay} seconds... (Attempt {attempt}/{retries})")
                    time.sleep(delay)
            raise Exception(f"Failed after {retries} attempts.")
        return wrapper
    return decorator
            

# Remove existing datasets before re-downloading
def clear_existing_datasets():
    deforestation_path = os.path.join(data_dir, "deforestation.csv")
    pollution_path = os.path.join(data_dir, "air_pollution.csv")
    
    if os.path.exists(deforestation_path):
        os.remove(deforestation_path)
        print("Removed existing deforestation dataset.")
    if os.path.exists(pollution_path):
        os.remove(pollution_path)
        print("Removed existing pollution dataset.")


# Download function for deforestation data
@retry_on_failure(retries=100, delay=5)
def download_data(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {file_path}")
    

# Download pollution data using Kaggle API with subprocess
@retry_on_failure(retries=100, delay=5)
def download_pollution_data():
    try:
        # Kaggle CLI download command
        kaggle_command = [
            venv_path,
            'datasets', 'download', '-d', 'danlessa/air-pollution-at-so-paulo-brazil-since-2013',
            '-p', data_dir, '--unzip'
        ]
        
        # Run the Kaggle download command
        subprocess.run(kaggle_command, check=True)
        
        # Find the extracted CSV file within the data directory
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith(".csv"):
                    pollution_file = os.path.join(root, file)
                    print(f"Pollution dataset downloaded and extracted to: {pollution_file}")
                    return pollution_file

        print("Pollution data extraction failed.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error downloading pollution data: {e}")
        return None
    

# Apply transformations to deforestation dataset
def clean_deforestation_data(df):
    
    # Focus only on major deforestation events
    df = df[df['data_type'] == 'defor']
    
    # Only keep date, ha_eck_iv, and shape_Area
    df = df.rename(columns={
        'date': 'Date',
        'ha_eck_iv': 'AffectedArea'
    })
    df = df[['Date', 'AffectedArea']]
    
    # Standardize the time format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S%z', errors='coerce')
    df['Date'] = df['Date'].dt.tz_localize(None) # Remove timezone information
    
    # Sort ascendingly by time
    df = df.sort_values(by='Date', ascending=True)
    
    # Drop unnecessary columns
    df = df.dropna(subset=['Date', 'AffectedArea'])
    
    # Aggregate by summing AffectedArea per month
    df = df.groupby(df['Date'].dt.to_period('M')).agg({'AffectedArea': 'sum'}).reset_index()
    df['Date'] = df['Date'].dt.to_timestamp()  # Convert period back to timestamp
    
    # Filter for the overlapping period
    df = df[(df['Date'] >= '2013-05-01') & (df['Date'] <= '2018-12-31')]
    
    return df


# Apply transformations to pollution dataset
def clean_pollution_data(df):
    # Change column names and align pollutant names with standard names
    df = df.rename(columns={df.columns[0]: 'No.', 'time': 'Date', 'id': 'ID', 'MP10': 'PM10', 'MP2.5': 'PM2.5', 'BENZENO': 'Benzene', 'TOLUENO': 'Toluene'})
    
    # Keep relevant columns only and standardize the time format
    df = df[['Date', 'PM10', 'TRS', 'O3', 'NO2', 'CO', 'PM2.5', 'SO2', 'Benzene', 'Toluene']]
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    
    # Drop rows with all empty pollutants data
    pollutant_columns = ['PM10', 'TRS', 'O3', 'NO2', 'CO', 'PM2.5', 'SO2', 'Benzene', 'Toluene']
    df = df.dropna(subset=pollutant_columns, how='all')
    
    # Ensure pollutant columns are numeric
    df[pollutant_columns] = df[pollutant_columns].apply(pd.to_numeric, errors='coerce')
    
    # Get an average by averaging per day
    df = df.groupby(df['Date'].dt.to_period('D')).mean(numeric_only=True).reset_index()
    df['Date'] = df['Date'].dt.to_timestamp() # Convert period back to timestamp
    
    # Get an average by averaging per month to align with deforestation dataset
    df = df.groupby(df['Date'].dt.to_period('M')).mean(numeric_only=True).reset_index()
    df['Date'] = df['Date'].dt.to_timestamp() # Convert period back to timestamp
    
    # Filter for the overlapping period
    df = df[(df['Date'] >= '2013-05-01') & (df['Date'] <= '2018-12-31')]
    
    return df


# Clear existing datasets, then download fresh ones
clear_existing_datasets()
deforestation_path = os.path.join(data_dir, "deforestation.csv")
pollution_data_path = download_pollution_data()

# Download deforestation data
download_data(deforestation_url, deforestation_path)

# Run data loading and save to SQLite if downloads succeed
if os.path.exists(deforestation_path) and pollution_data_path:
    # Load datasets
    deforestation_df = pd.read_csv(deforestation_path)
    pollution_df = pd.read_csv(pollution_data_path)
    
    # Apply transformations
    deforestation_df = clean_deforestation_data(deforestation_df)
    pollution_df = clean_pollution_data(pollution_df)
    
    # Save to deforestation.db
    deforestation_db_path = os.path.join(data_dir, "deforestation.db")
    try:
        conn = sqlite3.connect(deforestation_db_path)
        deforestation_df.to_sql("deforestation", conn, if_exists="replace", index=False)
        conn.close()
        print("Deforestation data saved to deforestation.db")
    except sqlite3.Error as e:
        print(f"Error saving deforestation data to SQLite: {e}")
    
    # Save to air_pollution.db
    pollution_db_path = os.path.join(data_dir, "air_pollution.db")
    try:
        conn = sqlite3.connect(pollution_db_path)
        pollution_df.to_sql("pollution", conn, if_exists="replace", index=False)
        conn.close()
        print("Pollution data saved to air_pollution.db")
    except sqlite3.Error as e:
        print(f"Error saving pollution data to SQLite: {e}")
    
    print("Data pipeline complete. Datasets saved to SQLite databases.")
else:
    print("Data download failed. Please check paths and Kaggle credentials.")
