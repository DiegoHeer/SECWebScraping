import requests


def get_cik_from_ticker(ticker):
    # Official SEC url that contains all the CIK x Ticker data
    base_url = 'https://www.sec.gov/include/ticker.txt'

    txt_content = requests.get(base_url).text

    mapping_dict = dict()
    for mapping in txt_content.split('\n'):
        company_ticker = mapping.split('\t')[0]
        company_cik = mapping.split('\t')[1]

        mapping_dict[company_ticker] = company_cik

    return mapping_dict[ticker.lower()]


# Only for testing purposes
if __name__ == '__main__':
    ticker = 'MSFT'
    cik_number = get_cik_from_ticker(ticker)
    print(f'The SEC sik number of {ticker} is: ' + cik_number)
