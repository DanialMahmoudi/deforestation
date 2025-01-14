import os
import sqlite3
import requests
import subprocess
import pandas as pd
import sys
import time
from functools import wraps
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random
import math


# To see whether CI works or not

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


# Generate mock data
def create_mock_data():
    # Mock deforestation data
    mock_deforestation = pd.DataFrame({
        'objectid': np.arange(53716, 53716 + 3),  # 12 mock rows starting from the provided objectid
        'date': pd.date_range(start='2013-07-31', periods=3, freq='M').strftime('%Y/%m/%d %H:%M:%S+00'),
        'data_type': ['defor'] * 3,  # All rows are of type 'degrad'
        'orig_oid': np.random.randint(0, 10, 3),
        'orig_fname': ['imazon_sad_degradacao_2014-07_amazonia.shp'] * 3,
        'gfwid': np.random.choice(['900D21D4-98A0-49CE-962F-8AAC8C6740FB', '541FAB70-B4B4-4A0C-8647-4231CA6D16FA', 
                                   '2C57D170-C76F-4784-977A-0C470BEE4E82', '9C5CDF75-10E5-4B1E-B198-1822447FE0C6'], 3),
        'globalid': np.random.choice(['{BBFDA6BE-3BAB-47C7-809F-1DDE5CE0FB91}', '{26DDC927-7941-41EC-BB6F-AB1E9A03A1FE}', 
                                      '{501ACF77-105F-43E3-8513-F7CCEF9AE8D3}', '{15936FD5-1FBA-473D-9E8E-AB326D376E1B}'], 3),
        'ha_eck_iv': np.random.uniform(5, 2000, 3),  # Random float values for hectares (within reasonable deforestation range)
        'date_alias': pd.date_range(start='2013-07-31', periods=3, freq='M').strftime('%Y/%m/%d %H:%M:%S+00'),
        'shape_Length': np.random.uniform(1000, 10000, 3),  # Mock shape length values
        'shape_Area': np.random.uniform(100000, 5000000, 3)  # Mock shape area values
    })
    mock_deforestation.to_csv(os.path.join(data_dir, 'deforestation.csv'), index=False)

    # Generate hourly time data for a full year (365 days)
    time_range = pd.date_range(start='2013-07-31 00:00:00', end='2013-08-31 00:00:00', freq='H')
    
    # Mock pollution data
    mock_pollution = pd.DataFrame({
        '': np.arange(0, len(time_range)),
        'time': time_range,
        'id': [65] * len(time_range),
        'MP10': np.nan,
        'TRS': np.nan,
        'O3': np.nan,
        'NO2': np.nan,
        'CO': np.nan,
        'MP2.5': np.nan,
        'SO2': np.nan,
        'BENZENO': np.nan,
        'TOLUENO': np.nan
    })
    # Randomly fill in missing values for pollutants (for demonstration purposes)
    for column in ['MP10', 'TRS', 'O3', 'NO2', 'CO', 'MP2.5', 'SO2', 'BENZENO', 'TOLUENO']:
        mock_pollution[column] = mock_pollution[column].apply(lambda x: random.uniform(5, 30) if random.random() > 0.2 else np.nan)
        
    # Save mock pollution data in the "cetesb.csv" folder
    cetesb_dir = os.path.join(data_dir, 'cetesb.csv')
    os.makedirs(cetesb_dir, exist_ok=True)  # Ensure the folder exists
    mock_pollution.to_csv(os.path.join(cetesb_dir, 'cetesb.csv'), index=False)
    print("Mock data created.")


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
        
        # Explicitly target cetesb.csv
        cetesb_file_path = os.path.join(data_dir, "cetesb.csv", "cetesb.csv")
        if os.path.exists(cetesb_file_path):
            print(f"Using pollution dataset: {cetesb_file_path}")
            return cetesb_file_path
        else:
            raise FileNotFoundError(f"'cetesb.csv' not found in {data_dir}")
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
    
    # Drop rows with missing values
    df = df.dropna(subset=['Date', 'AffectedArea'])
    
    # Aggregate by summing AffectedArea per month
    df = df.groupby(df['Date'].dt.to_period('M')).agg({'AffectedArea': 'sum'}).reset_index()
    df['Date'] = df['Date'].dt.to_timestamp()  # Convert period back to timestamp
    
    # Filter for the overlapping period
    df = df[(df['Date'] >= '2013-05-01') & (df['Date'] <= '2018-12-31')]
    
    # Setting the date as the index
    df.set_index('Date', inplace=True)
    
    # Reindex to fill missing months
    all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='MS')  # Monthly start frequency
    df = df.reindex(all_dates)
    
    # Interpolate missing values linearly
    df['AffectedArea'] = df['AffectedArea'].interpolate(method='linear')
    
    # Resetting index if needed
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)
    
    # Round values up to 2 decimal points
    df['AffectedArea'] = df['AffectedArea'].round(2)
    
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
    
    # Fill missing values in TRS, Benzene, and Toluene with 0
    columns_to_fill = ['TRS', 'Benzene', 'Toluene']
    df[columns_to_fill] = df[columns_to_fill].fillna(0)
    
    # Round values up to 2 decimal points
    numeric_columns = ['PM10', 'TRS', 'O3', 'NO2', 'CO', 'PM2.5', 'SO2', 'Benzene', 'Toluene']
    df[numeric_columns] = df[numeric_columns].round(2)

    return df

# Deforestation Trend Plot
def plot_deforestation_trend(deforestation_df):
    
    # Plot deforestation over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=deforestation_df, x="Date", y="AffectedArea", label="Deforestation Area")
    plt.title("Deforestation Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Affected Area (ha)")
    plt.tight_layout()
    plt.show()
    
# Function to plot deforestation trend with each pollutant
def plot_deforestation_with_pollutants(deforestation_df, pollution_df):
    save_dir = "data"
    
    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Plot deforestation trend with each pollutant one at a time
    for pollutant in pollution_df.columns.difference(['Date']):
        # Create a new figure for each pollutant
        plt.figure(figsize=(12, 6))
        
        # Plot deforestation trend with log transformation for showing purposes
        sns.lineplot(data=deforestation_df, x="Date", y=deforestation_df['AffectedArea'].apply(lambda x: 10 * math.log10(x + 1)), 
                     label="Log Deforestation Area", color="green")
        
        # Plot the pollutant trend with log transformation
        sns.lineplot(data=pollution_df, x="Date", y=pollution_df[pollutant].apply(lambda x: 10 * math.log10(x + 1)),
                     label=f"Log {pollutant}", color="red")
        
        # Set title and labels
        plt.title(f"Deforestation vs {pollutant} Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Values")
        plt.legend()
        
        # Save the plot as a PNG file
        plot_filename = os.path.join(save_dir, f"deforestation_vs_{pollutant}.png")
        plt.tight_layout()
        plt.savefig(plot_filename)
        
        # Show the plot
        plt.show()
    
# Trend Plot for all pollutants
def plot_pollutant_trends(pollution_df):
    
    # Plot each pollutant average based on time
    plt.figure(figsize=(15, 10))
    for col in pollution_df.columns.difference(['Date']):
        sns.lineplot(data=pollution_df, x="Date", y=col, label=col)
        
    plt.title("Trends of All Pollutants Over Time")
    plt.xlabel("Date")
    plt.ylabel("Pollutant Levels")
    plt.legend(title="Pollutants", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
    
# Correlation Heatmap
def plot_correlation_heatmap(deforestation_df, pollution_df):
    
    # Merge datasets
    merged_df = pd.merge(deforestation_df, pollution_df, on="Date", how="inner")
    
    #Plot correlation
    correlation_matrix = merged_df.drop(columns=['Date']).corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Correlation Between Deforestation and All Pollutants")
    plt.tight_layout()
    plt.show()
    
# Scatter plot for deforestation vs each pollutant
def plot_deforestation_vs_pollutant(deforestation_df, pollution_df, pollutants):
    
    # Merge datasets
    merged_df = pd.merge(deforestation_df, pollution_df, on="Date", how="inner")
    
    for pollutant in pollutants:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=merged_df, x=pollutant, y="AffectedArea")
        plt.title(f"Deforestation Area vs {pollutant}")
        plt.xlabel(f"{pollutant} Levels")
        plt.ylabel("Deforestation Area (ha)")
        plt.show()


# Clear existing datasets, then download fresh ones
clear_existing_datasets()
deforestation_path = os.path.join(data_dir, "deforestation.csv")
pollution_data_path = os.path.join(data_dir, "cetesb.csv", "cetesb.csv")

# Check if mock data should be used
if os.getenv('USE_MOCK_DATA') == 'true':
    create_mock_data()
else:
    # Download datasets
    download_data(deforestation_url, deforestation_path)
    pollution_data_path = download_pollution_data()

# Run data loading and save to SQLite if downloads succeed
if os.path.exists(deforestation_path) and pollution_data_path:
    # Load datasets
    deforestation_df = pd.read_csv(deforestation_path)
    pollution_df = pd.read_csv(pollution_data_path)
    
    # Apply transformations
    deforestation_df = clean_deforestation_data(deforestation_df)
    pollution_df = clean_pollution_data(pollution_df)
    
    # Calling visualization functions
    #plot_deforestation_with_pollutants(deforestation_df, pollution_df) ///////// Uncomment
    
    #plot_deforestation_trend(deforestation_df)
    #plot_pollutant_trends(pollution_df)
    #plot_correlation_heatmap(deforestation_df, pollution_df)
    #pollutants = pollution_df.columns.difference(['Date'])
    #plot_deforestation_vs_pollutant(deforestation_df, pollution_df, pollutants)
    
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
