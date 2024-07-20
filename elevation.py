import os
import gpxpy
import gpxpy.gpx
import numpy as np

# Function to extract elevation data from a GPX file
def extract_elevation_data():
    gpx_file_path = os.path.expanduser('~/marathonPacing/Boston_Marathon_Still_can_t_believe_that_s_a_real_thing_that_happened_.gpx')

    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    
    elevations = []
    distances = []

    def haversine(lon1, lat1, lon2, lat2):
        R = 6371  # Radius of the Earth in km
        dlon = np.radians(lon2 - lon1)
        dlat = np.radians(lon2 - lat1)
        a = np.sin(dlat / 2) * np.sin(dlat / 2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) * np.sin(dlon / 2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c  # Distance in km
        return distance

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

    distances = [d * 0.621371 for d in distances]  # Convert km to miles
    return distances, elevations

# Save the data for later use
distances, elevations = extract_elevation_data()
np.save('distances.npy', distances)
np.save('elevations.npy', elevations)

print("Distances and elevations data saved to distances.npy and elevations.npy")
