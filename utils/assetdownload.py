'''threaded module to download assets to local drive'''

import requests
import uuid
import os
from urllib.parse import urlparse

from concurrent.futures import ThreadPoolExecutor, as_completed

url_list = []

def add_url(url_nft : str ):
    url_list.append(url_nft)
 
def download_file(url, file_name):
    try:
        html = requests.get(url, stream=True)
        a = urlparse(url)
        open(f'assets/{os.path.basename(a.path)}', 'wb').write(html.content)
        return html.status_code
    except requests.exceptions.RequestException as e:
       return e
 
def runner():
    threads= []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in url_list:
            file_name = uuid.uuid1()
            threads.append(executor.submit(download_file, url, file_name))
            
        for task in as_completed(threads):
            print(task.result()) 