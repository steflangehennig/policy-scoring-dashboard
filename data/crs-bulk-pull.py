import csv
import os
import requests
from bs4 import BeautifulSoup

## see dev website: https://www.everycrsreport.com/download.html

# Download metadata file from everycrsreport.com
csv_url = 'https://www.everycrsreport.com/reports.csv'
csv_filename = 'reports.csv'
if not os.path.exists(csv_filename):
    response = requests.get(csv_url)
    with open(csv_filename, 'wb') as f:
        f.write(response.content)

# Parse reports.csv and download HTML files from latestHTML links
# Finish by converting to .txt files for model
base_url = 'https://www.everycrsreport.com/'
output_dir = 'txt'
os.makedirs(output_dir, exist_ok=True)

with open(csv_filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        html_path = row['latestHTML']
        if html_path:
            report_id = row['number']
            html_url = base_url + html_path
            try:
                html_response = requests.get(html_url)
                html_response.raise_for_status()
                soup = BeautifulSoup(html_response.content, 'html.parser')
                text = soup.get_text()
                text_filename = os.path.join(output_dir, f"{report_id}.txt")
                with open(text_filename, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
                print(f"Downloaded and converted: {report_id}")
            except requests.HTTPError as e:
                print(f"Failed to download {html_url}: {e}")
