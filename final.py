# Uses the Data ETL pipeline to answer the following question:
# From 2014-2024, did the number of travel articles by the NY Times referencing Barcelona rise and fall with FC Barcelona's placement in La Liga?

# Import necessary modules
import requests
import time
import csv
import pathlib

# Declare constants
API_KEY = "your-api"

URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

# The DATES constant is a dictionary with the beginning and end dates as key:value pairs for the 2014-2024 seasons of La Liga
DATES = {'20140823':'20150523', '20150821':'20160515', '20160819':'20170521', '20170818':'20180520', '20180817':'20190519', '20190816':'20200524', '20200912':'20210523', '20210813':'20220522', '20220812':'20230604', '20230811':'20240526'}

# Declare variables
params = {
    'api-key': API_KEY,
    'q': 'Barcelona',
    'fq': 'section.displayName.contains:("Travel") OR desk.contains:("Travel")'
}

# The data variable holds a list of dictionaries with the season year and final standing for FC Barcelona from 2014-2024
# It will be modified to have a 'Hits' key with the value being the number of travel articles referencing Barcelona during that season
data = [{'Season':'2014-2015', 'Standing':'1'}, {'Season':'2015-2016', 'Standing':'1'}, {'Season':'2016-2017', 'Standing':'2'}, {'Season':'2017-2018', 'Standing':'1'}, {'Season':'2018-2019', 'Standing':'1'}, {'Season':'2019-2020', 'Standing':'2'}, {'Season':'2020-2021', 'Standing':'3'}, {'Season':'2021-2022', 'Standing':'2'}, {'Season':'2022-2023', 'Standing':'1'}, {'Season':'2023-2024', 'Standing':'2'}]

def get_hits(begin, end, params):
    """Returns the number of hits for given dates and parameters

    Args:
        begin (string): Beginning date for article search
        end (string): Ending date for article search
        params (dictionary): Other parameters for article search

    Returns:
        int: The number of hits that are returned from the given parameters
    """
    params['begin_date'] = begin
    params['end_date'] = end
    content = requests.get(URL, params=params).json()
    return content['response']['metadata']['hits']

# Main
if __name__ == "__main__":
    counter = 0
    # Creates and fills 'Hits' key in all data dicts using get_hits function
    for begin, end in DATES.items():
        data[counter]['Hits'] = get_hits(begin, end, params)
        counter += 1
        time.sleep(12)
    
    # Creates csv file and writes all data to it
    cwd = pathlib.Path.cwd()
    file = cwd/"final.csv"
    file.touch()
    with file.open(mode='w', encoding='utf-8',newline='') as python_final:
        writer = csv.DictWriter(python_final, fieldnames = ["Season", "Standing", "Hits"])
        writer.writeheader()
        writer.writerows(data)
