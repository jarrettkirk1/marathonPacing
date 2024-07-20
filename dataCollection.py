import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the main results page
url = "https://results.baa.org/2024/?event_main_group=runner&num_results=25&pid=list&pidp=start&search%5Bsex%5D=M&search%5Bage_class%5D=%25&event=R&favorite_remove=9TGHS6FF19F091"

# Send a GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract runner detail page links
runner_links = []
for a_tag in soup.find_all('a', href=True):
    if "content=detail" in a_tag['href']:
        runner_links.append(a_tag['href'])

print(f"Found {len(runner_links)} runner links.")

# Base URL for constructing full URLs
base_url = "https://results.baa.org/2024/"

# List to store data
runners_data = []

# Loop through each runner's link and scrape the "min_km" data
for link in runner_links:
    runner_url = base_url + link
    runner_response = requests.get(runner_url)
    runner_soup = BeautifulSoup(runner_response.content, 'html.parser')
    
    # Extract athlete's name
    name_tag = runner_soup.find('td', class_='f-__fullname')
    athlete_name = name_tag.text.strip() if name_tag else 'Unknown'
    
    # Extract "min_km" data from the correct table
    splits_table = runner_soup.find('div', class_='box-splits').find('tbody')
    if splits_table:
        for row in splits_table.find_all('tr'):
            split = row.find('th', class_='desc').text.strip()
            min_km = row.find('td', class_='min_km').text.strip() if row.find('td', class_='min_km') else None
            split_data = {
                'Athlete Name': athlete_name,
                'Split': split,
                'min_km': min_km
            }
            runners_data.append(split_data)

# Convert to DataFrame
df = pd.DataFrame(runners_data, columns=['Athlete Name', 'Split', 'min_km'])

# Pivot the data
pivot_df = df.pivot(index='Athlete Name', columns='Split', values='min_km').reset_index()

# Specify the order of columns
column_order = ['Athlete Name', '5K', '10K', '15K', '20K', 'HALF', '25K', '30K', '20 Miles', '21 Miles', '35K', '23 Miles', '24 Miles', '40K', '25.2 Miles', 'Finish Net']

# Reorder the columns
pivot_df = pivot_df[column_order]

# Display the DataFrame
print(pivot_df.head())

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")

# Save to CSV
csv_path = os.path.join(os.getcwd(), 'boston_marathon_min_km_pivoted.csv')
pivot_df.to_csv(csv_path, index=False)
print(f"CSV file saved at: {csv_path}")
