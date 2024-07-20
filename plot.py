import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function to load pacing data from a CSV file
def load_pacing_data(csv_file_path):
    pacing_df = pd.read_csv(csv_file_path)
    
    # Prepare the pacing data
    pacing_df = pacing_df.melt(id_vars=['Athlete Name'], var_name='Split', value_name='Split Time')
    
    # Convert Split to numeric distances
    def convert_split_to_distance(split):
        if 'K' in split:
            return int(split.split(' ')[0].replace('K', '')) * 0.621371
        elif split == 'HALF':
            return 13.1
        elif split == 'Finish':
            return 26.2
        elif 'Miles' in split:
            return float(split.split(' ')[0])
        else:
            return np.nan
    
    pacing_df['Split Distance'] = pacing_df['Split'].apply(convert_split_to_distance)
    pacing_df['Split Time (seconds)'] = pd.to_timedelta(pacing_df['Split Time']).dt.total_seconds()
    
    # Calculate the time difference between consecutive splits
    pacing_df['Time Diff (seconds)'] = pacing_df.groupby('Athlete Name')['Split Time (seconds)'].diff().fillna(0)
    
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

    # Get the first athlete's data
    first_athlete = pacing_df['Athlete Name'].unique()[0]
    athlete_df = pacing_df[pacing_df['Athlete Name'] == first_athlete]

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot the elevation profile
    ax1.plot(distances, elevations, label='Elevation Profile', color='blue')
    ax1.fill_between(distances, elevations, color='lightblue', alpha=0.5)
    ax1.set_xlabel('Distance (miles)')
    ax1.set_ylabel('Elevation (feet)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Plot the split times as red dots
    ax1.scatter(athlete_df['Split Distance'], athlete_df['Time Diff (seconds)'] / 60, color='red', label='Split Time (min)')

    # Add titles and legends
    plt.title('Boston Marathon Elevation Profile with Split Times')
    fig.tight_layout()  # To ensure the labels don't overlap
    fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

    # Show the plot
    plt.show()

# Run the plot function
plot_elevation_and_pacing()
