import requests
import pickle
import os
from utils import load, save, api_key
from pprint import pprint

FILE = 'data\\market_data.pkl'

def market_data():
    if os.path.isfile(FILE):
        data = load(FILE)
        print("Market data loaded.")
    else:
        base_url = 'https://data-api.defipulse.com/api/v1/'
        added_url = 'defipulse/api/MarketData'
        params = {
            'api-key': api_key('defipulse')
        }
        r = requests.get(base_url + added_url, params=params)
        data = r.json()
        print("Market data downloaded.")
        save(data, FILE)
    return data

def types(market_data):
    return list(market_data.keys())

def values(market_data):
    keys = types(market_data)
    return [market_data[key]['value']['total']['USD']['value'] for key in keys]

def leaders(market_data):
    keys = types(market_data)
    return [market_data[key]['dominance_name'] for key in keys]

def leader_value(market_data):
    keys = types(market_data)
    return [market_data[key]['dominance_value'] for key in keys]

def leader_percentage(market_data):
    keys = types(market_data)
    return [market_data[key]['dominance_pct'] for key in keys]

if __name__ == '__main__':
    d = market_data()
    names = types(d)
    values = values(d)
    leaders = leaders(d)
