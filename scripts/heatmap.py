import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm

# Function to load pacing data from a CSV file
def load_pacing_data(csv_file_path):
    pacing_df = pd.read_csv(csv_file_path)
    
    # Convert Split to numeric distances
    def convert_split_to_distance(split):
        if 'K' in split:
            return int(split.replace('K', '')) * 0.621371
        elif split == 'HALF':
            return 13.1
        elif split == 'Finish Net':
            return 26.2
        elif 'Miles' in split:
            return float(split.split(' ')[0])
        else:
            return np.nan
    
    # Ensure the columns are in the desired order
    desired_order = ['Athlete Name', '5K', '10K', '15K', '20K', 'HALF', '25K', '30K', '20 Miles', '21 Miles', '35K', '23 Miles', '24 Miles', '40K', '25.2 Miles', 'Finish Net']
    pacing_df = pacing_df[desired_order]
    
    # Create a list of split distances in the same order as the columns in the CSV file
    split_distances = [convert_split_to_distance(split) for split in desired_order if split != 'Athlete Name']
    
    return pacing_df, split_distances

# Function to load elevation data from .npy files
def load_elevation_data():
    distances = np.load('distances.npy')
    elevations = np.load('elevations.npy')
    return distances, elevations

# Convert pace string to numeric value (e.g., "4:30" to 4.5)
def convert_pace_to_numeric(pace_str):
    if isinstance(pace_str, str):
        parts = pace_str.split(':')
        return float(parts[0]) + float(parts[1]) / 60
    return pace_str

# Convert Split to numeric distances (function moved outside)
def convert_split_to_distance(split):
    if 'K' in split:
        return int(split.replace('K', '')) * 0.621371
    elif split == 'HALF':
        return 13.1
    elif split == 'Finish Net':
        return 26.2
    elif 'Miles' in split:
        return float(split.split(' ')[0])
    else:
        return np.nan

# Main function to plot the elevation and pacing data
def plot_elevation_and_pacing_heatmap():
    distances, elevations = load_elevation_data()
    csv_file_path = 'boston_marathon_min_km_pivoted.csv'
    pacing_df, split_distances = load_pacing_data(csv_file_path)

    # Convert pacing data to numeric values
    pacing_df.iloc[:, 1:] = pacing_df.iloc[:, 1:].applymap(convert_pace_to_numeric)
    
    # Create a DataFrame for the heatmap
    heatmap_data = pd.melt(pacing_df, id_vars=['Athlete Name'], var_name='Split', value_name='min_km')
    heatmap_data['Distance'] = heatmap_data['Split'].apply(lambda x: convert_split_to_distance(x))
    heatmap_data = heatmap_data.dropna(subset=['min_km', 'Distance'])

    # Use tqdm to show progress during data preparation
    with tqdm(total=len(heatmap_data), desc="Preparing heatmap data") as pbar:
        heatmap_data_list = []
        for idx, row in heatmap_data.iterrows():
            heatmap_data_list.append(row)
            pbar.update(1)

    heatmap_df = pd.DataFrame(heatmap_data_list)

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot the elevation profile
    ax1.plot(distances, elevations, label='Elevation Profile', color='blue')
    ax1.fill_between(distances, elevations, color='lightblue', alpha=0.5)
    ax1.set_xlabel('Distance (miles)')
    ax1.set_ylabel('Elevation (feet)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis for the heatmap
    ax2 = ax1.twinx()

    # Create the heatmap using seaborn histplot
    sns.histplot(
        data=heatmap_df,
        x='Distance',
        y='min_km',
        bins=(len(split_distances), 50),
        pmax=1.0,
        cmap='Reds',
        ax=ax2
    )

    ax2.set_ylabel('Pace (min/mile)', color='red')
    ax2.set_ylim(7.0, 4.5)  # Inverse scale for pace
    ax2.tick_params(axis='y', labelcolor='red')

    # Add titles and legends
    plt.title('Boston Marathon Elevation Profile with Pacing Heatmap')
    fig.tight_layout()  # To ensure the labels don't overlap
    fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

    # Show the plot
    plt.show()

# Run the plot function
plot_elevation_and_pacing_heatmap()
