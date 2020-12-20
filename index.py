import requests
import urllib
from bs4 import BeautifulSoup


# Function that makes building url's easy
def make_url(base_url, comp):
    url = base_url

    # add each component to the base url
    for r in comp:
        url = '{}/{}'.format(url, r)

    return url


# Base url for the daily index files
base_url = r'https://www.sec.gov/Archives/edgar/daily-index'
components = ['886982', '000156459019011378', '0001564590-19-011378-index-headers.html']

# Create the daily index url for 2019
year_url = make_url(base_url, ['2019', 'index.json'])

# Request the 2019 url
content = requests.get(year_url)
decoded_content = content.json()

# Loop through the dictionary
for item in decoded_content['directory']['item']:

    # get the name of the folder
    print('-'*100)
    print('Pulling url for quarter {}'.format(item['name']))

    # Create the qtr url
    qtr_url = make_url(base_url, ['2019', item['name'], 'index.json'])

    print(qtr_url)
    # Request the url and decode it
    file_content = requests.get(qtr_url)
    decoded_content = file_content.json()

    print('-'*100)
    print('Pulling files')

    for file in decoded_content['directory']['item']:
        file_url = make_url(base_url, ['2019', item['name'], file['name']])
        print(file_url)


