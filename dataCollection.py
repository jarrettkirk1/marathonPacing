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

# Loop through each runner's link and scrape the splits data
for link in runner_links:
    runner_url = base_url + link
    runner_response = requests.get(runner_url)
    runner_soup = BeautifulSoup(runner_response.content, 'html.parser')
    
    # Extract athlete's name
    name_tag = runner_soup.find('td', class_='f-__fullname')
    athlete_name = name_tag.text.strip() if name_tag else 'Unknown'
    
    # Extract splits data from the correct table
    splits_table = runner_soup.find('div', class_='box-splits').find('tbody')
    if splits_table:
        for row in splits_table.find_all('tr'):
            split_data = {
                'Athlete Name': athlete_name,
                'Split': row.find('th', class_='desc').text.strip(),
                'Split Time': row.find('td', class_='time').text.strip()
            }
            runners_data.append(split_data)

# Convert to DataFrame
df = pd.DataFrame(runners_data, columns=['Athlete Name', 'Split', 'Split Time'])

# Pivot the data
pivot_df = df.pivot(index='Athlete Name', columns='Split', values='Split Time').reset_index()

# Display the DataFrame
print(pivot_df.head())

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")

# Save to CSV
csv_path = os.path.join(os.getcwd(), 'boston_marathon_splits_pivoted.csv')
pivot_df.to_csv(csv_path, index=False)
print(f"CSV file saved at: {csv_path}")
