import pickle
import configparser
from datetime import datetime, timedelta

def save(object_to_save, file):
    with open(file, 'wb') as f:
        pickle.dump(object_to_save, f)

def load(file):
    with open(file, 'rb') as f:
        asset = pickle.load(f)
    return asset

def api_key(provider):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[provider]['token']

def convert_timestamp(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp).strftime('%d-%m-%Y')

def compare_projects(projects1, projects2):
    p1 = [i['name'] for i in projects1]
    p2 = [i['name'] for i in projects2]
    p1 = [i.lower().strip().replace(' ', '-') for i in p1]
    p1 = [i.lower().strip().replace(' ', '-') for i in p2]
    def replace_set(dataset):
        data = []
        for name in dataset:
            if '.' in name and '-' in name:
                data.append(name.replace('.', ''))
            elif '.' in name and not '-' in name:
                data.append(name.replace('.', '-'))
            else:
                data.append(name)
        return data
    p1 = replace_set(p1)
    p2 = replace_set(p2)
    unique = [name for name in p1 if name not in p2]
    return unique
