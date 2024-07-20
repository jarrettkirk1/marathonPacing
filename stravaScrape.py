import requests
from bs4 import BeautifulSoup

# URL of the Strava segment page
url = 'https://www.strava.com/segments/965206'  # Replace with the actual URL

# Send a GET request to fetch the raw HTML content
response = requests.get(url)
if response.status_code == 200:
    print("Successfully fetched the page")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <td> elements containing <a> tags with href attributes
td_elements = soup.find_all('td')

# List to store all activity_ids
activity_ids = []

# Iterate through all matching elements and extract activity_id
for td_element in td_elements:
    a_tag = td_element.find('a', href=True)
    if a_tag and '/activities/' in a_tag['href']:
        # Extract the href attribute and split to get the activity_id
        href = a_tag['href']
        activity_id = href.split('/activities/')[1]
        activity_ids.append(activity_id)

# Print all extracted activity_ids
for idx, activity_id in enumerate(activity_ids, start=1):
    print(f'Activity ID {idx}: {activity_id}')
