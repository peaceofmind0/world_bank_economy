#config data for world bank API

base_url = 'https://api.worldbank.org/v2'
per_page = 1000
format = 'json'
lang = 'en'
# Indicator codes
indicators = {
    "GDP (current US$)": "NY.GDP.MKTP.CD",
    "Population": "SP.POP.TOTL",
    "Number of exporter": "A1"
}

