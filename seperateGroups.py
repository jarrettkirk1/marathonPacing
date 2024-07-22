import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
    split_distances = [0] + [convert_split_to_distance(split) for split in desired_order if split != 'Athlete Name']
    
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

# Main function to plot the elevation and pacing data
def plot_elevation_and_pacing():
    distances, elevations = load_elevation_data()
    csv_file_path = 'boston_marathon_min_km_pivoted.csv'
    pacing_df, split_distances = load_pacing_data(csv_file_path)

    # Convert pacing data to numeric values
    pacing_df.iloc[:, 1:] = pacing_df.iloc[:, 1:].applymap(convert_pace_to_numeric)
    
    # Split data into quartiles based on 'Finish Net' time
    finish_times = pacing_df['Finish Net'].apply(convert_pace_to_numeric)
    pacing_df['Finish Time'] = finish_times
    quartiles = pd.qcut(pacing_df['Finish Time'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    pacing_df['Quartile'] = quartiles

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot the elevation profile
    ax1.plot(distances, elevations, label='Elevation Profile', color='blue')
    ax1.fill_between(distances, elevations, color='lightblue', alpha=0.5)
    ax1.set_xlabel('Distance (miles)')
    ax1.set_ylabel('Elevation (feet)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xlim([0, distances.max()])
    ax1.set_ylim([elevations.min(), elevations.max()])

    # Remove gap between the elevation plot and the y-axis
    ax1.margins(x=0)

    # Create a second y-axis for the pacing data
    ax2 = ax1.twinx()

    # Plot median and standard deviation for each quartile group
    for quartile in ['Q1', 'Q2', 'Q3', 'Q4']:
        quartile_df = pacing_df[pacing_df['Quartile'] == quartile]
        median_pace = [quartile_df.iloc[:, 1:-2].median().iloc[0]] + list(quartile_df.iloc[:, 1:-2].median())
        std_pace = [quartile_df.iloc[:, 1:-2].std().iloc[0]] + list(quartile_df.iloc[:, 1:-2].std())
        
        # Plot median
        ax2.plot(split_distances, median_pace, label=f'Median Pace - {quartile}', linestyle='--')
        
        # Plot standard deviation as shaded area
        ax2.fill_between(split_distances, np.array(median_pace) - np.array(std_pace), np.array(median_pace) + np.array(std_pace), alpha=0.3)

    ax2.set_ylabel('Pace (min/mile)', color='red')
    ax2.set_ylim(18.0, 3.0)  # Adjusted pace range
    ax2.tick_params(axis='y', labelcolor='red')

    # Format the right y-axis to show time in "minutes:seconds/mile"
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}:{int((x-int(x))*60):02d}'))

    # Add titles and legends
    plt.title('Boston Marathon Elevation Profile with Median and Standard Deviation of Pacing Data')
    fig.tight_layout()  # To ensure the labels don't overlap
    fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

    # Show the plot
    plt.show()

# Run the plot function
plot_elevation_and_pacing()
