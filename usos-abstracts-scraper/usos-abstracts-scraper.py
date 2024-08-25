from fp.fp import FreeProxy
from lxml import html
import requests
import json
from random import randint
from time import sleep

proxy = FreeProxy(rand=True, anonym=True).get()

proxies = {
    "http": proxy,
    "https": proxy
}

print(proxies)

with open("usos-abstracts-scraper/thesis_data.json", "a") as file:
    #file.write("[") 
    for thesis_id in range(1, 100): # max 16940 
        url = f"https://apd.usos.pwr.edu.pl/diplomas/{thesis_id}"

        response = requests.get(url, proxies=proxies, timeout=10, headers={"User-Agent":"Mozilla/5.0", "Accept": "application/json"})

        print(response)

        tree = html.fromstring(response.content)

        thesis_data = {
            "thesis_id": thesis_id,
            "pl_title": ' '.join(tree.xpath("//*[@id=\"thesisInfo\"]/tbody/tr[2]/td[2]/div/div[1]/div[2]/text()")).strip(),
            "en_title": ' '.join(tree.xpath("//*[@id=\"thesisInfo\"]/tbody/tr[2]/td[2]/div/div[2]/div[2]/text()")).strip(),
            "thesis_promotor": ' '.join(tree.xpath("//*[@id=\"thesisInfo\"]/tbody/tr[4]/td[2]/div/span/a/text()")).strip(),
            "pl_abstract": ' '.join(tree.xpath("//*[@id=\"thesisInfo\"]/tbody/tr[8]/td[2]/div/div[1]/div[2]/text()")).strip(),
            "en_abstract": ' '.join(tree.xpath("//*[@id=\"thesisInfo\"]/tbody/tr[8]/td[2]/div/div[2]/div[2]/text()")).strip(),
            "pl_keywords": ' '.join(tree.xpath("//*[@id=\"thesisInfo\"]/tbody/tr[9]/td[2]/div/div[1]/div[2]/text()")).strip(),
            "en_keywords": ' '.join(tree.xpath("//*[@id=\"thesisInfo\"]/tbody/tr[9]/td[2]/div/div[2]/div[2]/text()")).strip()
        }
        if thesis_id > 1:
            file.write(",")
            
        json.dump(thesis_data, file, indent=6)
        
        sleep(randint(5,10))
    #file.write("]")
