import requests
import os
from utils import load, save
from pprint import pprint

def get_protocols(update=False):
    FILE = 'data\\llama_projects.pkl'
    if os.path.isfile(FILE) and not update:
        data = load(FILE)
        print("Market data loaded.")
    else:
        url = 'https://api.llama.fi/protocols'
        r = requests.get(url)
        data = r.json()
        print("Market data downloaded.")
        save(data, FILE)
    return data

def download_images(p_data):
    logos = [i['logo'] for i in p_data]
    counter = 0
    for logo in logos:
        if logo:
            file_name = logo.split('/')[-1]
            file_path = 'static\\img\\' + file_name
            if not os.path.isfile(file_path):
                with requests.get(logo, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                counter += 1
    if counter > 0:
        print(f"{counter} images downloaded.")

def sort_protocols(protocols_dataset, sorting_value, reverse=False):
    return sorted(protocols_dataset, key= lambda item: item[sorting_value], reverse=reverse)

if __name__ == '__main__':
    p = get_protocols()
    #names = [i['name'] for i in p]
    #images = [i['logo'] for i in p]
    #download_images(p)
