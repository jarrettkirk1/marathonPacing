import numpy as np
import matplotlib.pyplot as plt

# Function to load elevation data from .npy files
def load_elevation_data():
    distances = np.load('distances.npy')
    elevations = np.load('elevations.npy')
    return distances, elevations

# Main function to plot the elevation data
def plot_elevation():
    distances, elevations = load_elevation_data()

    # Plot the elevation profile
    plt.figure(figsize=(12, 6))
    plt.plot(distances, elevations, label='Elevation Profile', color='blue')
    plt.fill_between(distances, elevations, color='lightblue', alpha=0.5)
    plt.xlabel('Distance (miles)')
    plt.ylabel('Elevation (feet)')
    plt.title('Boston Marathon Elevation Profile')
    plt.legend()
    plt.show()

# Run the plot function
plot_elevation()
