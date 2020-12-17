# Youtube tutorial to web scrape US public companies financial documents
import requests
import cik_ticker_mapping
from bs4 import BeautifulSoup

# Define our base url
base_url = r"https://www.sec.gov/Archives/edgar/data"

# Define a CIK number to do a company search, in this example GOLDMAN SACHS
cik_num = '/' + str(cik_ticker_mapping.get_cik_from_ticker('GS')) + '/'

# let's create a filing url
filings_url = base_url + cik_num + '/index.json'

# request the url
content = requests.get(filings_url)
decoded_content = content.json()

# go and grab a single filing number
filing_number = decoded_content['directory']['item'][0]['name']

# Define our filing number url
filing_url = base_url + cik_num + filing_number + '/index.json'

# Request the filing url
content = requests.get(filing_url)
document_content = content.json()

# get the document names
for document in document_content['directory']['item']:
    if document['type'] != 'image2.gif':
        doc_name = document['name']
        document_url = base_url + cik_num + filing_number + '/' + doc_name
        print(document_url)

