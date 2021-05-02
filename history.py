import requests
from utils import load, save, api_key, convert_timestamp
import os
from pprint import pprint

def get_history(project, period, resolution='days'):
    FILE = 'data\\' + 'history_' + str(project) + '_' + str(period) + '.pkl'
    if os.path.isfile(FILE):
        data = load(FILE)
        print("Market data loaded.")
    else:
        base_url = 'https://data-api.defipulse.com/api/v1/'
        added_url = 'defipulse/api/GetHistory'
        params = {
            'api-key': api_key('defipulse'),
            'project': project,
            'period': period,
            'resolution': resolution
        }
        r = requests.get(base_url + added_url, params=params)
        data = r.json()
        print("Market data downloaded.")
        save(data, FILE)
    return data

def create_dataset(history_data, value_point='tvlUSD'):
    value_points = ['tvlUSD', 'tvlETH', 'BTC', 'ETH', 'DAI']
    if value_point in value_points:
        return [[convert_timestamp(i['timestamp']), i[value_point]] for i in history_data]
    else:
        return "Selected value point is not in the downloaded dataset."

if __name__ == '__main__':
    project = 'alpha-homora'
    period = 'all'
    resolution = 'days'
    #h = get_history(project, period, resolution='hours')
    #for i in h:
    #    i['timestamp'] = convert_timestamp(i['timestamp'])
    #ho = [convert_timestamp(i['timestamp']) for i in h]
    #data = create_dataset(h)
    #for i in range(30):
    #    print(data[i][0], ' - ', format(data[i][1], ',d'))
    base_url = 'https://data-api.defipulse.com/api/v1/'
    added_url = 'defipulse/api/GetHistory'
    params = {
        'api-key': api_key('defipulse'),
        'project': project,
        'period': period,
        'resolution': resolution
    }
    r = requests.get(base_url + added_url, params=params)
    print(r)
