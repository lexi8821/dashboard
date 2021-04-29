import requests
import pickle
import os
from pprint import pprint
import math
from utils import load, save, api_key

def get_projects():
    FILE = 'data\\projects.pkl'
    if os.path.isfile(FILE):
        projects = load(FILE)
        print("Projects loaded.")
    else:
        base_url = 'https://data-api.defipulse.com/api/v1/'
        added_url = 'defipulse/api/GetProjects'
        params = {
            'api-key': api_key('defipulse'),
        }
        r = requests.get(base_url + added_url, params=params)
        projects = r.json()
        print("Projects downloaded.")
        save(projects, FILE)
    return projects

def get_names(projects):
    names = dict()
    for proj in projects:
        names[proj['name']] = proj['value']['total']['USD']['value']
    return names

def get_values(projects):
    assets = dict()
    for proj in projects:
        assets[proj['name']] = [proj['value']['tvl']['BTC']['value'],
            proj['value']['tvl']['ETH']['value'],
            proj['value']['tvl']['USD']['value']]
    return assets

def splitter(list_to_split, no_of_parts, which_part_to_return=None):
    units_in_part = math.ceil(len(list_to_split) / no_of_parts)
    test = lambda list_to_split, units_in_part: [list_to_split[i: i + units_in_part] for i in range(0, len(list_to_split), units_in_part)]
    if not which_part_to_return:
        return test(list_to_split, units_in_part)
    else:
        return test(list_to_split, units_in_part)[which_part_to_return - 1]

def sort_projects(projects_dataset):
    pass

def vals(projects, denomination):
    denominations = ['BTC', 'ETH', 'USD']
    if denomination in denominations:
        return [[proj['name'], proj['value']['tvl'][denomination]['value']] for proj in projects]
    else:
        return ["Wrong denomination"]

if __name__ == '__main__':
    projects = get_projects()
    #categories = sorted(list(set([item['category'] for item in projects])))
    #chains = sorted(list(set([item['chain'] for item in projects])))
    #websites = []
    #for i in range(len(projects)):
    #    try:
    #        websites.append(projects[i]['website'])
    #    except:
    #        continue

    #values_dict = get_values(projects)
    #btcs = [int(i[0]) for i in values_dict.values()]
    #eths = [int(i[1]) for i in values_dict.values()]
    #usds = [i[2] for i in values_dict.values()]
    #names = list(values_dict.keys())
    #s_dict = len(values_dict)
    #splitter = 4
    #xx = [i for i in range(1, 88)]
    #t = splitter(list(values_dict.keys()), 4)
    #for i in t:
    #    print(i)
    usd = vals(projects, 'USD')
    eth = vals(projects, 'ETH')
    btc = vals(projects, 'BTC')
