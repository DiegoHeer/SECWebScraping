import requests
import pandas as pd
from bs4 import BeautifulSoup

# define the base url needed to create the file url
base_url = r'https://www.sec.gov'

# url obtained from the second tutorial for 10k's
text_file_10k = 'https://www.sec.gov/Archives/edgar/data/1265107/0001265107-19-000004.txt'

# change url to json type
json_file_10k = text_file_10k.replace("-", '')
json_file_10k = json_file_10k.replace(".txt", '/index.json')

# request the url and decode it
content = requests.get(json_file_10k).json()

for file in content['directory']['item']:

    # Grab the filing summary and create a new url leading to the file se we can download it
    if file['name'] == 'FilingSummary.xml':
        xml_summary = base_url + content['directory']['name'] + '/' + file['name']

        # print('-' * 100)
        # print('File Name: ' + file['name'])
        # print('File Path: ' + xml_summary)

# Parsing the Filing Summary
# define a new base url that represents the filing folder, for downloading the reports
base_url = xml_summary.replace('FilingSummary.xml', '')

# request and parse the content
content = requests.get(xml_summary).content
soup = BeautifulSoup(content, features='lxml')

# Find the 'myreports' tag, bacause this contains all the individual reports submitted
reports = soup.find('myreports')

# Create a master list, with all the individual components of the report
master_reports = []

# Loop through each report in the 'myreports' tag but avoid the last one (error)
for report in reports.find_all('report')[:-1]:
    # Create a dictionary to store all the different parts required
    report_dict = {}
    report_dict['name_short'] = report.shortname.text
    report_dict['name_long'] = report.longname.text
    report_dict['position'] = report.position.text
    report_dict['category'] = report.menucategory.text
    report_dict['url'] = base_url + report.htmlfilename.text

    # append the dictionary to the master list
    master_reports.append(report_dict)

    # Print the info to the user
    # print('-' * 100)
    # print(base_url + report.htmlfilename.text)
    # print(report.longname.text)
    # print(report.shortname.text)
    # print(report.menucategory.text)
    # print(report.position.text)

# create the list to hold the statement urls
statements_url = []

for report_dict in master_reports:

    # Define the statements required
    item1 = r'Consolidated Balance Sheets'
    item2 = r'Consolidated Statements of Operations and Comprehensive Income (Loss)'
    item3 = r'Consolidated Statements of Cash Flows'
    item4 = r"Consolidated Statements of Stockholder's (Deficit) Equity"

    # store them in a list
    report_list = [item1, item2, item3, item4]

    # if the short name can be found in the report list
    if report_dict['name_short'] in report_list:
        # print some info and store it in the statements_url
        # print('_' * 100)
        # print(report_dict['name_short'])
        # print(report_dict['url'])
        statements_url.append(report_dict['url'])

# Put all the statements in a single data set
master_data = []

# loop through each statement url
for statement in statements_url:

    # Define a dictionary that will store the different parts of the statements
    statement_data = {}
    statement_data['headers'] = []
    statement_data['sections'] = []
    statement_data['data'] = []

    # request the statement file content
    content = requests.get(statement).content
    report_soup = BeautifulSoup(content, 'html.parser')

    # find all the rows, figure out what type of row if is, parse, and store in the statment file list
    for index, row in enumerate(report_soup.table.find_all('tr')):

        # first get all the elements
        cols = row.find_all('td')

        # if it's a regular row and not a section or a table header
        if len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0:
            regular_row = [element.text.strip() for element in cols]
            statement_data['data'].append(regular_row)

        # if it's a regular row and a section but not a table header
        elif len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0:
            section_row = cols[0].text.strip()
            statement_data['sections'].append(section_row)

        # if it's not any of those it must be a header
        elif len(row.find_all('th')) != 0:
            header_row = [element.text.strip() for element in row.find_all('th')]
            statement_data['headers'].append(header_row)

        else:
            print('Error encountered!')

    # append it to the master list
    master_data.append(statement_data)

# Converting the master data into a dataframe
# Grab the proper component
income_headers = master_data[1]['headers'][1]
income_data = master_data[1]['data']

# Put the data in a Dataframe
income_df = pd.DataFrame(income_data)

# Define the index column and rename it, removing the old column after reindex
income_df.index = income_df[0]
income_df.index.name = 'Category'
income_df = income_df.drop(0, axis=1)

# Get rid of the '$' and other stuff
income_df = income_df.replace('[\$,)]', '', regex=True) \
    .replace('[(]', '-', regex=True) \
    .replace('', 'NaN', regex=True)

# convert everything that is still a string to float
income_df = income_df.astype(float)

# Change column headers
income_df.columns = income_headers

# # Display
# print('-' * 100)
# print('Before indexing')
# print('-' * 100)
# print(income_df)

# Put the income statement in a xlsx file
income_df.to_excel('test_file.xlsx', sheet_name='Income Statements')
