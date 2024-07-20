import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import numpy as np

# Load the GPX file
gpx_file_path = '/mnt/data/Boston_Marathon_Still_can_t_believe_that_s_a_real_thing_that_happened_.gpx'
with open(gpx_file_path, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Extract elevation data
elevations = []
distances = []

# Helper function to calculate distance between two points
def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Radius of the Earth in km
    dlon = np.radians(lon2 - lon1)
    dlat = np.radians(lat2 - lat1)
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c  # Distance in km
    return distance

# Iterate through track points
total_distance = 0
previous_point = None
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if previous_point:
                distance = haversine(previous_point.longitude, previous_point.latitude, point.longitude, point.latitude)
                total_distance += distance
            else:
                total_distance = 0  # Start from 0 for the first point
            
            distances.append(total_distance)
            elevations.append(point.elevation)
            previous_point = point

# Convert distances from km to miles
distances = [d * 0.621371 for d in distances]  # 1 km = 0.621371 miles

# Plot the elevation profile
plt.figure(figsize=(12, 6))
plt.plot(distances, elevations, label='Elevation Profile', color='blue')
plt.fill_between(distances, elevations, color='lightblue')
plt.xlabel('Distance (miles)')
plt.ylabel('Elevation (feet)')
plt.title('Boston Marathon Elevation Profile')
plt.legend()
plt.show()
