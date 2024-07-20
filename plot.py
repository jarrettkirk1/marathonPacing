import os
import matplotlib.pyplot as plt
import pandas as pd
from elevation import extract_elevation_data
from dataCollection import load_pacing_data

# Main function to plot the elevation and pacing data
def plot_elevation_and_pacing(gpx_file_path, csv_file_path):
    distances, elevations = extract_elevation_data(gpx_file_path)
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

# File paths
gpx_file_path = os.path.expanduser('~/marathonPacing/Boston_Marathon_Still_can_t_believe_that_s_a_real_thing_that_happened_.gpx')
csv_file_path = 'boston_marathon_splits_pivoted.csv'

# Run the plot function
plot_elevation_and_pacing(gpx_file_path, csv_file_path)
