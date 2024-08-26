from fp.fp import FreeProxy
from lxml import html
from fake_useragent import UserAgent
from random import randint
from time import sleep
import requests
import json
import os

ua = UserAgent()

proxy = FreeProxy(rand=True, anonym=True).get()

proxies = {
    'http': proxy
}

current_directory = os.getcwd()

if 'usos-abstracts-scraper' in os.path.basename(current_directory):
    file_path = os.path.join(current_directory, 'theses_data.json')
else:
    file_path = os.path.join(current_directory, 'usos-abstracts-scraper', 'theses_data.json')

thesis_No = 0

first_thesis_id = int(input('Input initial thesis id - minimum 1: '))
last_thesis_id = int(input('Input final thesis id - maximum 16946 as of 26/08/2024: ')) 

if first_thesis_id == last_thesis_id:
    last_thesis_id += 1

theses_list = []

for thesis_id in range(first_thesis_id, last_thesis_id): 
    url = f'https://apd.usos.pwr.edu.pl/diplomas/{thesis_id}'

    # generate fake User-Agents
    fake_ua = ua.random

    response = requests.get(url, proxies=proxies, timeout=5, headers={'User-Agent': fake_ua, 'Accept': 'application/json'})

    thesis_No += 1

    print(thesis_No, response)

    tree = html.fromstring(response.content)

    thesis_data = {
        'thesis_id': thesis_id,
        'pl_title': ' '.join(tree.xpath('//*[@id=\'thesisInfo\']/tbody/tr[2]/td[2]/div/div[1]/div[2]/text()')).strip(),
        'en_title': ' '.join(tree.xpath('//*[@id=\'thesisInfo\']/tbody/tr[2]/td[2]/div/div[2]/div[2]/text()')).strip(),
        'thesis_promotor': ' '.join(tree.xpath('//*[@id=\'thesisInfo\']/tbody/tr[4]/td[2]/div/span/a/text()')).strip(),
        'pl_abstract': ' '.join(tree.xpath('//*[@id=\'thesisInfo\']/tbody/tr[8]/td[2]/div/div[1]/div[2]/text()')).strip(),
        'en_abstract': ' '.join(tree.xpath('//*[@id=\'thesisInfo\']/tbody/tr[8]/td[2]/div/div[2]/div[2]/text()')).strip(),
        'pl_keywords': ' '.join(tree.xpath('//*[@id=\'thesisInfo\']/tbody/tr[9]/td[2]/div/div[1]/div[2]/text()')).strip(),
        'en_keywords': ' '.join(tree.xpath('//*[@id=\'thesisInfo\']/tbody/tr[9]/td[2]/div/div[2]/div[2]/text()')).strip()
    }
        
    theses_list.append(thesis_data)

    sleep(randint(2,5))

with open(file_path, 'a') as file:
    json.dump(theses_list, file, sort_keys=True, indent=4, separators=(',', ': '))