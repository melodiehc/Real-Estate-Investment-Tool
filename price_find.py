import requests, json, csv
url = 'https://www.zillow.com'

def price_find(url):
    #This function takes an input of a URL and resturns the listing price
    #The site it mines is Zillow
    #The input must be a string 
    payload = {
        'source' : 'universal'
        'url' : url,
        'user_agent_type':'desktop',
        'render': 'html',
        'browser_instructions' : [
            {
                'type': 'fetch_resource',
                'filter': 'https://www.zillow.com/async-create-search-page-state'
            }
        ]
    }