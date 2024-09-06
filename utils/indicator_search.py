import requests as rq
import pandas as pd

def indicator_search(key_word):
    '''
    Return a catalog of indicators that contain key words
    keyword(str): a key word. Examples: GDP, Number of Exporters
    '''
    response_json = rq.get('https://api.worldbank.org/v2/indicator/?per_page=100000&format=json').json()[1]
    df_indicator = pd.DataFrame(response_json)
    df_indicator['name'] = df_indicator['name'].astype(str)
    return df_indicator[df_indicator['name'].str.contains(key_word)]

indicator_search('Number of Exporters')