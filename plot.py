import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function to load pacing data from a CSV file
def load_pacing_data(csv_file_path):
    pacing_df = pd.read_csv(csv_file_path)
    
    # Prepare the pacing data
    pacing_df = pacing_df.melt(id_vars=['Athlete Name'], var_name='Split', value_name='Split Time')
    pacing_df['Split Distance'] = pacing_df['Split'].apply(lambda x: int(x.split(' ')[0].replace('K', '')) * 0.621371 if 'K' in x else 13.1 if 'HALF' in x else 26.2 if 'Finish' in x else x)
    pacing_df['Split Time (seconds)'] = pd.to_timedelta(pacing_df['Split Time']).dt.total_seconds()
    
    return pacing_df

# Function to load elevation data from .npy files
def load_elevation_data():
    distances = np.load('distances.npy')
    elevations = np.load('elevations.npy')
    return distances, elevations

# Main function to plot the elevation and pacing data
def plot_elevation_and_pacing():
    distances, elevations = load_elevation_data()
    csv_file_path = 'boston_marathon_splits_pivoted.csv'
    pacing_df = load_pacing_data(csv_file_path)

    # Plot the elevation profile
    plt.figure(figsize=(12, 6))
    plt.plot(distances, elevations, label='Elevation Profile', color='blue')
    plt.fill_between(distances, elevations, color='lightblue', alpha=0.5)
    plt.xlabel('Distance (miles)')
    plt.ylabel('Elevation (feet)')
    plt.title('Boston Marathon Elevation Profile with Pacing Data')

    # Overlay the pacing data
    athletes = pacing_df['Athlete Name'].unique()
    for athlete in athletes:
        athlete_df = pacing_df[pacing_df['Athlete Name'] == athlete]
        plt.plot(athlete_df['Split Distance'], athlete_df['Split Time (seconds)'], label=f'{athlete} Pacing')

    plt.legend()
    plt.show()

# Run the plot function
plot_elevation_and_pacing()
