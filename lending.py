import requests
from utils import load, save, api_key, convert_timestamp
import os
from pprint import pprint

def get_lending_history(period, resolution='days'):
    FILE = 'data\\' + 'lending_history_' + '_' + str(period) + '.pkl'
    if os.path.isfile(FILE):
        data = load(FILE)
        print("Dataset loaded.")
    else:
        base_url = 'https://data-api.defipulse.com/api/v1/'
        added_url = 'defipulse/api/getLendingHistory'
        params = {
            'api-key': api_key('defipulse'),
            'period': period,
            'resolution': resolution
        }
        r = requests.get(base_url + added_url, params=params)
        data = r.json()
        print("Dataset downloaded.")
        save(data, FILE)
    return data

def get_lending_projects():
    FILE = 'data\\lending_projects.pkl'
    if os.path.isfile(FILE):
        data = load(FILE)
        print("Dataset loaded.")
    else:
        base_url = 'https://data-api.defipulse.com/api/v1/'
        added_url = 'defipulse/api/GetLendingProjects'
        params = {
            'api-key': api_key('defipulse'),
        }
        r = requests.get(base_url + added_url, params=params)
        data = r.json()
        print("Dataset downloaded.")
        save(data, FILE)
    return data

def get_lending_marketdata():
    FILE = 'data\\lending_marketdata.pkl'
    if os.path.isfile(FILE):
        data = load(FILE)
        print("Dataset data loaded.")
    else:
        base_url = 'https://data-api.defipulse.com/api/v1/'
        added_url = 'defipulse/api/LendingMarketData'
        params = {
            'api-key': api_key('defipulse'),
        }
        r = requests.get(base_url + added_url, params=params)
        data = r.json()
        print("Dataset downloaded.")
        save(data, FILE)
    return data

def get_lending_tokens():
    FILE = 'data\\lending_tokens.pkl'
    if os.path.isfile(FILE):
        data = load(FILE)
        print("Dataset data loaded.")
    else:
        base_url = 'https://data-api.defipulse.com/api/v1/'
        added_url = 'defipulse/api/GetLendingTokens'
        params = {
            'api-key': api_key('defipulse'),
        }
        r = requests.get(base_url + added_url, params=params)
        data = r.json()
        print("Dataset downloaded.")
        save(data, FILE)
    return data

def get_rates(token, amount, update=False):
    FILE = 'data\\lending_rates_' + str(token) + '_' + str(amount) + '.pkl'
    if os.path.isfile(FILE) and not update:
        data = load(FILE)
        print("Dataset data loaded.")
    else:
        base_url = 'https://data-api.defipulse.com/api/v1/'
        added_url = 'defipulse/api/GetRates'
        params = {
            'api-key': api_key('defipulse'),
            'token': token,
            'amount': amount
        }
        r = requests.get(base_url + added_url, params=params)
        data = r.json()
        print("Dataset downloaded.")
        save(data, FILE)
    return data

def transform_rates(rate_response):
    dataset = dict()
    dataset['token_name'] = rate_response['token']['name']
    dataset['token_price'] = rate_response['token']['price']
    exchanges = list(rate_response['rates'].keys())
    exchanges = [rate_response['rates'][exchange] for exchange in rate_response['rates'].keys()]
    dataset['exchanges'] = exchanges
    return dataset

def _finditem(obj, key):
    if key in obj: return obj[key]
    for exchange in obj['exchanges']:
        for k, v in exchange.items():
            if isinstance(v, dict):
                item = _finditem(v, key)
                if item is not None:
                    return item

if __name__ == '__main__':
    #lh = get_lending_history('all')
    #print("Lending History")
    #print(lh[0]['lend_rates'])
    #print(30*'-')
    lp = get_lending_projects()
    #pprint("Lending projects")
    pprint(lp[0])
    #print(30*'-')
    #ld = get_lending_marketdata()
    #print("Lending market data")
    #print(ld.keys())
    #print(30*'-')
    #lt = get_lending_tokens()
    #print("Lending tokens")
    #print(lt)
    #print(30*'-')
    #token = 'DAI'
    #lr = get_rates(token, 1000, update=True)
    #print(f"Lending Rates for {token}")
    #pprint(lr)
    #print(30*'-')
    #f = transform_rates(lr)
    #pprint(f)
    #x = _finditem(f, 'rate')
