
import requests as rq
import pandas as pd
import duckdb
import numpy as np
from utils.api_funcs import url_params,load_response,clean_indicator_df


#region and country data
#get a list of region

region_url = url_params(endpoint='region')
df_all_region = load_response(region_url)
df_standard_region = df_all_region[df_all_region['id'] != '']
#reset index to start from 1
df_standard_region =  df_standard_region.reset_index(drop=True)
df_standard_region['index'] = df_standard_region.index + 1
df_standard_region = df_standard_region.rename(columns={'index':'region_id','code':'region_code','iso2code':'region_iso2_code','name':'region_name'})
df_standard_region


#get a list of country

country_url = url_params(endpoint= 'country')
df_country= load_response(country_url)

#exclude aggregated region from country list
df_country = df_country[df_country['region'].apply(lambda x: x['value']) != 'Aggregates']

# Reset the index and drop the old one
df_country = df_country.reset_index(drop=True)  
df_country.index = df_country.index + 1 

#add region code and income level
df_country['region_code'] = df_country['region'].apply(lambda x: x['id'])

df_country['income_level'] = df_country['incomeLevel'].apply(lambda x : x['value'])
df_country['lending_type'] = df_country['lendingType'].apply(lambda x: x['value'])
df_country_select = df_country[['id','iso2Code','name','region_code','income_level','lending_type']]

#add region id for each country by joining with region table
df_country_select = df_country_select.rename(columns={'id':'country_code','iso2Code':'country_iso2_code','name':'country_name'})

df_country_merge = pd.merge(df_country_select,df_standard_region,left_on='region_code',right_on='region_code',how = 'inner')
df_country_merge = df_country_merge[['country_code','country_iso2_code','country_name','region_id','income_level','lending_type']]
df_country_merge['country_id'] = df_country_merge.index + 1
df_country_merge


#indicator data
#GDP for all countries 

gdp_url = url_params(endpoint = 'country',indicator = "GDP (current US$)")
df_country_gdp = load_response(gdp_url)
df_country_gdp_merged = clean_indicator_df(df_country_merge, df_country_gdp)

#Use billion dollar as unit
df_country_gdp_merged['GDP_billion_dollar'] = df_country_gdp_merged['value']/1e+09 

df_country_gdp_select = df_country_gdp_merged[['country_name_x','country_id','country_iso2_code','countryiso3code','date','GDP_billion_dollar']]
df_country_gdp_select = df_country_gdp_select.rename(columns={'country_name_x':'country_name','countryiso3code':'country_iso3_code','date':'year'})
df_country_gdp_select['country_gdp_id'] = df_country_gdp_select.index + 1
df_country_gdp_select

#Population for all countries

population_url = url_params(endpoint='country',indicator='Population')
df_country_population = load_response(population_url)
df_country_population_merged = clean_indicator_df(df_country_merge,df_country_population)
df_country_population_select = df_country_population_merged[['country_name_x','country_id','country_iso2_code','countryiso3code','date','value']]
df_country_population_select = df_country_population_select.rename(columns={'country_name_x':'country_name','countryiso3code':'country_iso3_code','date':'year','value':'population'})
df_country_population_select['country_population_id'] = df_country_population_select.index + 1
df_country_population_select

#Number of exporters for all countries

exporter_url = url_params(endpoint='country',indicator='Number of exporter')
df_exporter = load_response(exporter_url)
df_exporter_merged = clean_indicator_df(df_country_merge,df_exporter)
df_exporter_merged = df_exporter_merged[['country_name_x','country_id','country_iso2_code','countryiso3code','date','value']]
df_exporter_merged = df_exporter_merged.rename(columns={'country_name_x':'country_name','countryiso3code':'country_iso3_code','date':'year','value':'number_of_exporter'})
df_exporter_merged['country_exporter_id'] = df_exporter_merged.index + 1
df_exporter_merged


#load data to duckdb
conn = duckdb.connect(database='world_bank_economy.duckdb')
conn.execute("""
    CREATE OR REPLACE TABLE region (
    region_ID INTEGER PRIMARY KEY,
    region_code VARCHAR,
    region_iso2_code VARCHAR,
    region_name VARCHAR
    );
             
    CREATE OR REPLACE TABLE country(
        country_id INTEGER PRIMARY KEY,
        country_iso3_code VARCHAR,
        country_iso2_code VARCHAR,
        country_name VARCHAR,
        region_ID INTEGER,
        income_level VARCHAR,
        lending_type VARCHAR
    );
    
    CREATE OR REPLACE TABLE country_gdp(
        country_gdp_id INTEGER PRIMARY KEY,
        country_name VARCHAR,
        country_id INTEGER,
        gdp_billion_dollar FLOAT,
        YEAR INTEGER
    );
             
    CREATE OR REPLACE TABLE country_population(
        country_population_id INTEGER PRIMARY KEY,
        country_name VARCHAR,
        country_id VARCHAR,
        year INTEGER,
        population INTEGER,
    );
    
    CREATE OR REPLACE TABLE country_exporter(
        country_exporter_id INTEGER PRIMARY KEY,
        country_name VARCHAR,
        country_id VARCHAR,
        year INTEGER,
        number_of_exporter INTEGER
    );
             
    INSERT INTO region SELECT region_id,region_code,region_iso2_code,region_name FROM df_standard_region;
    
    INSERT INTO country SELECT country_id, country_code, country_iso2_code, country_name, region_id, income_level, lending_type from df_country_merge;

    INSERT INTO country_gdp SELECT country_gdp_id, country_name, country_id, GDP_billion_dollar, year FROM df_country_gdp_select;

    INSERT INTO country_population SELECT country_population_id, country_name, country_id, year, population FROM df_country_population_select;
    
    INSERT INTO country_exporter SELECT country_exporter_id, country_name, country_id, year, number_of_exporter from df_exporter_merged;
    """
             
)
conn.commit()
conn.close()

