import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Base URL for the results pages
base_url = "https://results.baa.org/2024/?page={}&event=R&event_main_group=runner&num_results=1000&pid=list&search%5Bsex%5D=M&search%5Bage_class%5D=%25"

# Function to get runner links from a page
def get_runner_links(page_number):
    url = base_url.format(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract runner detail page links
    runner_links = []
    for a_tag in soup.find_all('a', href=True):
        if "content=detail" in a_tag['href']:
            runner_links.append(a_tag['href'])
    
    print(f"Found {len(runner_links)} runner links on page {page_number}.")
    return runner_links

# Function to scrape splits data from a runner's page
def scrape_runner_data(runner_url):
    base_url = "https://results.baa.org/2024/"
    runner_response = requests.get(base_url + runner_url)
    runner_soup = BeautifulSoup(runner_response.content, 'html.parser')
    
    # Extract athlete's name
    name_tag = runner_soup.find('td', class_='f-__fullname')
    athlete_name = name_tag.text.strip() if name_tag else 'Unknown'
    
    # Extract splits data from the correct table
    splits_table = runner_soup.find('div', class_='box-splits').find('tbody')
    splits_data = []
    if splits_table:
        for row in splits_table.find_all('tr'):
            split = row.find('th', class_='desc').text.strip()
            min_km = row.find('td', class_='min_km').text.strip()
            splits_data.append({
                'Athlete Name': athlete_name,
                'Split': split,
                'min_km': min_km
            })
    return splits_data

# List to store data
all_runners_data = []

# Function to process each page
def process_page(page_number):
    runner_links = get_runner_links(page_number)
    page_runners_data = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_runner_data, link) for link in runner_links]
        for future in tqdm(as_completed(futures), total=len(futures), desc=f"Processing page {page_number}"):
            try:
                runner_data = future.result()
                page_runners_data.extend(runner_data)
            except Exception as e:
                print(f"Error scraping runner data: {e}")
    
    return page_runners_data

# Loop through each page to collect runner data using multithreading
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_page, page_number) for page_number in range(1, 16)]
    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing all pages"):
        try:
            page_runners_data = future.result()
            all_runners_data.extend(page_runners_data)
        except Exception as e:
            print(f"Error processing page: {e}")

# Convert to DataFrame
df = pd.DataFrame(all_runners_data, columns=['Athlete Name', 'Split', 'min_km'])

# Convert min_km to numeric, setting errors='coerce' to handle non-numeric values
df['min_km'] = pd.to_numeric(df['min_km'].str.replace(':', '.'), errors='coerce')

# Handle duplicates by taking the mean of duplicate entries
df = df.groupby(['Athlete Name', 'Split'], as_index=False).mean()

# Pivot the data
pivot_df = df.pivot(index='Athlete Name', columns='Split', values='min_km').reset_index()

# Ensure the columns are in the desired order
desired_order = ['Athlete Name', '5K', '10K', '15K', '20K', 'HALF', '25K', '30K', '20 Miles', '21 Miles', '35K', '23 Miles', '24 Miles', '40K', '25.2 Miles', 'Finish Net']
pivot_df = pivot_df.reindex(columns=desired_order)

# Display the DataFrame
print(pivot_df.head())

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")

# Save to CSV
csv_path = os.path.join(os.getcwd(), 'boston_marathon_min_km_pivoted.csv')
pivot_df.to_csv(csv_path, index=False)
print(f"CSV file saved at: {csv_path}")
