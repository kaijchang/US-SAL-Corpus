import requests
from bs4 import BeautifulSoup

import os
import subprocess
import re

DOWNLOAD_DIR = 'pdfs'

def download_file_if_needed(url: str):
    file_name = os.path.basename(url)
    if not os.path.exists(os.path.join(DOWNLOAD_DIR, file_name)):
        subprocess.run(['wget', '-P', DOWNLOAD_DIR, url])
    else:
        print(f'File {file_name} already exists')

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Volumes 1-64 from the Library of Congress
for i in range(1, 65):
    if i not in list(range(6, 9)):
        URL = f'https://www.loc.gov/item/llsl-v{i}'
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')

        for resource in soup.find_all(class_='resource'):
            resource_urls: list[str] = [option['value'] for option in resource.find_all('option')]

            for resource_url in resource_urls:
                file_name = os.path.basename(resource_url)
                if file_name.endswith('pdf') and re.match(r'^llsl-c\d{1,3}(?:s\d{1,3})?(?:-s\d{1,3})?\.pdf$', file_name):
                    download_file_if_needed(resource_url)

# Volumes 65-132 from GovInfo
for i in range(65, 133):
    download_file_if_needed(f'https://www.govinfo.gov/content/pkg/STATUTE-{i}/pdf/STATUTE-{i}.pdf')
