import os
import sqlite3
import requests
import subprocess
import pandas as pd
import sys

# Detect virtual environment path dynamically
venv_path = os.path.join(sys.prefix, 'Scripts', 'kaggle.exe') if os.name == 'nt' else os.path.join(sys.prefix, 'bin', 'kaggle')

# Set up paths
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

deforestation_url = "https://hub.arcgis.com/api/v3/datasets/9c4a16f9520447349159fa30abcea08b_2/downloads/data?format=csv&spatialRefId=3857&where=1%3D1"

# Download function for deforestation data
def download_data(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

# Download pollution data using Kaggle API with subprocess
def download_pollution_data():
    try:
        # Define download path for Kaggle
        download_dir = 'data'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Kaggle CLI download command
        kaggle_command = [
            venv_path,
            'datasets', 'download', '-d', 'danlessa/air-pollution-at-so-paulo-brazil-since-2013',
            '-p', download_dir, '--unzip'
        ]
        
        # Run the Kaggle download command
        subprocess.run(kaggle_command, check=True)

        # Find the extracted csv file within the data directory
        for root, dirs, files in os.walk(download_dir):
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
    # Rename columns
    df = df.rename(columns={
        'objectid': 'ID', 
        'date': 'Date', 
        'data_type': 'DataType', 
        'orig_oid': 'OrigOID',
        'orig_fname': 'OrigFname', 
        'gfwid': 'GFWID', 
        'globalid': 'GlobalID', 
        'ha_eck_iv': 'HaEckIV', 
        'date_alias': 'DateAlias', 
        'shape_Length': 'ShapeLength', 
        'shape_Area': 'ShapeArea'
    })
    
    # Convert Date column to datetime, handling time zone info
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S%z', errors='coerce')
    
    # Remove the timezone information
    df['Date'] = df['Date'].dt.tz_localize(None)
    
    # Sort by Date in ascending order
    df = df.sort_values(by='Date', ascending=True)

    # Handle missing values 
    df = df.dropna(subset=['Date', 'HaEckIV'])  # Drop rows where critical columns are missing

    return df

# Apply transformations to pollution dataset
def clean_pollution_data(df):
    # Rename 0th column to 'No.'
    df = df.rename(columns={df.columns[0]: 'No.', 'time': 'Time', 'id': 'ID'})

    # Convert 'time' column to datetime
    df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')  # Correct datetime format

    # Specify the pollutant columns
    pollutant_columns = ['MP10', 'TRS', 'O3', 'NO2', 'CO', 'MP2.5', 'SO2', 'BENZENO', 'TOLUENO']

    # Remove rows where all pollutant columns are NaN
    df = df.dropna(subset=pollutant_columns, how='all')
    
    # Ensure correct data types for pollutant columns (convert to float)
    df[pollutant_columns] = df[pollutant_columns].apply(pd.to_numeric, errors='coerce')

    return df

# Download data
deforestation_path = os.path.join(data_dir, "deforestation.csv")
pollution_data_path = download_pollution_data()
print(pollution_data_path)

# Run data loading and save to SQLite if downloads succeed
if pollution_data_path:
    download_data(deforestation_url, deforestation_path)
    
    if os.path.exists(deforestation_path):
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
    print("Pollution data download failed. Please check Kaggle credentials and path permissions.")
