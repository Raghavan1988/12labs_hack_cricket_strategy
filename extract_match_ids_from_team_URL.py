import re
import json
from bs4 import BeautifulSoup
import sys


import requests

def get_html_content(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        print ("error")
        return f"Failed to retrieve content, status code: {response.status_code}"


html = get_html_content(sys.argv[1])
team = sys.argv[2]


soup = BeautifulSoup(html, 'html.parser')


w = open(team + ".txt", "w")
for a in soup.find_all('a', href=True):
    url = a['href']

    if (url.endswith("full-scorecard")):
        pattern = r"/series/.+-(\d+)/.+-(\d+)/"

        match = re.search(pattern, url)
        if match:
            series_id = match.group(1)
            match_id = match.group(2)
            print(series_id, match_id)
            
            print(url)
            w.write(series_id + "," + match_id + "\n")

w.close()
