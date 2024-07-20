import os
import gpxpy

# Path to the GPX file
gpx_file_path = os.path.expanduser('/Users/jarrettkirk/marathonPacing/Boston_marathon_debut_2_11_18_.gpx')

# Function to read the GPX file and print the elevation of the first point
def check_start_elevation(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # Check the first point's elevation
    if gpx.tracks:
        first_track = gpx.tracks[0]
        if first_track.segments:
            first_segment = first_track.segments[0]
            if first_segment.points:
                first_point = first_segment.points[0]
                print(f"Elevation at the start of the race: {first_point.elevation} feet")
            else:
                print("No points found in the first segment.")
        else:
            print("No segments found in the first track.")
    else:
        print("No tracks found in the GPX file.")

# Run the function
check_start_elevation(gpx_file_path)
