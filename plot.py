import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    
    # Create a list of split distances in the same order as the columns in the CSV file
    split_distances = [convert_split_to_distance(split) for split in pacing_df.columns if split != 'Athlete Name']
    
    return pacing_df, split_distances

# Function to load elevation data from .npy files
def load_elevation_data():
    distances = np.load('distances.npy')
    elevations = np.load('elevations.npy')
    return distances, elevations

# Convert pace string to numeric value (e.g., "4:30" to 4.5)
def convert_pace_to_numeric(pace_str):
    parts = pace_str.split(':')
    return float(parts[0]) + float(parts[1]) / 60

# Format numeric pace to string (e.g., 4.5 to "4:30")
def format_numeric_to_pace(pace_numeric):
    minutes = int(pace_numeric)
    seconds = int((pace_numeric - minutes) * 60)
    return f'{minutes}:{seconds:02d}'

# Main function to plot the elevation and pacing data
def plot_elevation_and_pacing():
    distances, elevations = load_elevation_data()
    csv_file_path = 'boston_marathon_min_km_pivoted.csv'
    pacing_df, split_distances = load_pacing_data(csv_file_path)

    # Get the first athlete's data
    first_athlete = pacing_df.iloc[0]
    athlete_name = first_athlete['Athlete Name']
    min_mile_values = first_athlete[1:]  # Exclude the 'Athlete Name' column

    # Print out all the plot points
    print("Plot points (distance, min/mile):")
    for distance, min_mile in zip(split_distances, min_mile_values):
        if not pd.isna(min_mile):
            min_mile_numeric = convert_pace_to_numeric(min_mile)
            print(f"Distance: {distance:.2f} miles, Pace: {min_mile} min/mile (Numeric: {min_mile_numeric:.2f})")
    
    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot the elevation profile
    ax1.plot(distances, elevations, label='Elevation Profile', color='blue')
    ax1.fill_between(distances, elevations, color='lightblue', alpha=0.5)
    ax1.set_xlabel('Distance (miles)')
    ax1.set_ylabel('Elevation (feet)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis for the pacing data
    ax2 = ax1.twinx()

    # Define the pace range
    min_pace = 4.5  # Minimum pace (min/mile)
    max_pace = 7.0  # Maximum pace (min/mile)
    
    # Plot red dots at the split distances and corresponding min_mile values
    for distance, min_mile in zip(split_distances, min_mile_values):
        if not pd.isna(min_mile):
            min_mile_numeric = convert_pace_to_numeric(min_mile)
            ax2.scatter(distance, min_mile_numeric, color='red')
    
    ax2.set_ylabel('Pace (min/mile)', color='red')
    ax2.set_ylim(max_pace, min_pace)  # Set pace scale inversely
    ax2.tick_params(axis='y', labelcolor='red')

    # Format the right y-axis to show time in "minutes:seconds/mile"
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: format_numeric_to_pace(x)))

    # Add titles and legends
    plt.title('Boston Marathon Elevation Profile with Pacing Data')
    fig.tight_layout()  # To ensure the labels don't overlap
    fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

    # Show the plot
    plt.show()

# Run the plot function
plot_elevation_and_pacing()
