import requests as rq
import pandas as pd
from .api_config import base_url,per_page,format,lang,indicators

def url_params(params = {},endpoint ='country',indicator = None):
    '''
    Arguments:
        params (dict): paramaters for the API call, including per_page, format, lang, etc. Global parameters provided outside the func
        endpoint: the data point being pulled. Examples: country, region
        indicator: the indicator of a country. Examples: GDP, Population
    Returns:
        The formatted url based on configured parameters that is used for API call.
    '''
    params = {}
    params['per_page'] = per_page
    params['format'] = format
    params['lang'] = lang
    string_params = '&'.join([f'{key}={value}' for key, value in params.items()])
    if endpoint == 'country' and indicator: 
        #indicator can only be retrieved at a country but not a regional level
        indicator_code = indicators[indicator]
        url = f'{base_url}/{endpoint}/all/indicator/{indicator_code}?{string_params}'
    else: 
        #no indicator
        url = f'{base_url}/{endpoint}/all?{string_params}'
    return url


def load_response(url_init):
    '''
    Arguments:
        url: the url of the API call
    Returns:
        a dataframe of response data in raw form
    '''
    page = 1
    all_response = []
    url_page = url_init
    while True:
        try:
            url_page =  f'{url_init}&page={page}'
            response = rq.get(url_page)
            response.raise_for_status()
            response_json = response.json()
            page_data = response_json[1]
            all_response.extend(page_data)
            total_pages = response_json[0]['pages']
            if page >= int(total_pages):
                break
            page += 1    
        except rq.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except rq.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except rq.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except rq.exceptions.RequestException as err:
            print(f"Error: {err}")
    if all_response:
        df = pd.DataFrame(all_response)
        return df

def clean_indicator_df (df_country,df_indicator):
    '''
    Arguments:
        df_country: the country table with unique id. cols: country_name, country_id, country_iso2_code
        df_indicator: the dataframe for an indicator directly pulled from the API. cols: country
    Returns:
        an indicator dataframe that was cleaned and merged with the country dataframe, with country_id.
    '''
    #get country code and country name from raw data
    df_indicator['iso2Code'] = df_indicator['country'].apply(lambda x: x['id'])
    df_indicator['country_name'] = df_indicator['country'].apply(lambda x: x['value'])

    #join with the country table 
    df_indicator_merged = pd.merge(df_indicator,df_country,left_on='iso2Code',right_on='country_iso2_code',how = 'inner')

    #validate the join. should show countries codes are matching
    if len(df_indicator_merged[df_indicator_merged ['countryiso3code'] != df_indicator_merged ['country_code']]) != 0:
        raise Exception ('the indicator dataset country iso3 codes have discrepancies with the country list')
    
    return df_indicator_merged


