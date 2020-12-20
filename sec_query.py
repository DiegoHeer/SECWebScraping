import requests
from bs4 import BeautifulSoup

# Defining the parameters of the search
# base url for the SEC EDGAR browser
endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

# Define our parameters dictionary
param_dict = {'action': 'getcompany',
              'CIK': '1265107',
              'type': '10-k',
              'dateb': '20200101',
              'start': '',
              'output': 'atom',
              'count': '100'}

# request the url, and parse the response
response = requests.get(url=endpoint, params=param_dict)
soup = BeautifulSoup(response.content, features='lxml')

# Let the user know it was successful
# print('Request successful')
print(response.url)

# Parse data in url
# Find all the entry tags
entries = soup.find_all('entry')

# initialize our list for storage
master_list_xml = []

# loop through each found entry
for entry in entries:
    # grab the accession number to create the key value
    accession_number = entry.find('accession-number').text

    # create a new dictionary
    entry_dict = {}
    entry_dict[accession_number] = {}

    # store the category info
    category_info = entry.find('category')
    entry_dict[accession_number]['category'] = {}
    entry_dict[accession_number]['category']['label'] = category_info['label']
    entry_dict[accession_number]['category']['scheme'] = category_info['scheme']
    entry_dict[accession_number]['category']['term'] = category_info['term']

    # store the file info
    entry_dict[accession_number]['file_info'] = {}
    entry_dict[accession_number]['file_info']['act'] = entry.find('act').text
    entry_dict[accession_number]['file_info']['file_number'] = entry.find('file-number').text
    entry_dict[accession_number]['file_info']['file_number_href'] = entry.find('file-number-href').text
    entry_dict[accession_number]['file_info']['filing_date'] = entry.find('filing-date').text
    entry_dict[accession_number]['file_info']['filing_href'] = entry.find('filing-href').text
    entry_dict[accession_number]['file_info']['filing_type'] = entry.find('filing-type').text
    entry_dict[accession_number]['file_info']['form_number'] = entry.find('film-number').text
    entry_dict[accession_number]['file_info']['form_name'] = entry.find('form-name').text
    entry_dict[accession_number]['file_info']['file_size'] = entry.find('size').text

    # store extra info
    entry_dict[accession_number]['request_info'] = {}
    entry_dict[accession_number]['request_info']['link'] = entry.find('link')['href']
    entry_dict[accession_number]['request_info']['title'] = entry.find('title').text
    entry_dict[accession_number]['request_info']['last_updated'] = entry.find('updated').text

    # store in the master list
    master_list_xml.append(entry_dict)

    # print('-'*100)
    # print(entry.find('form-name').text)
    # print(entry.find('file-number').text)
    # print(entry.find('file-number-href').text)
    # print(entry.find('link')['href'])

# Parsing next page
# Find the link that will take us to the next page
# links = soup.find_all('link', {'rel': 'next'})
#
# # exclude the type parameter in the parameter dictionary
# del param_dict['type']
#
# # while there is still a next page
# while soup.find_all('link', {'rel': 'next'}) != []:
#     # grab the link
#     next_page_link = links[0]['href']
#
#     print('-' * 100)
#     print(next_page_link)
#
#     # request the next page
#     response = requests.get(url=next_page_link)
#     soup = BeautifulSoup(response.content, 'lxml')
#
#     # see if there is a next link
#     links = soup.find_all('link', {'rel': 'next'})
