from fp.fp import FreeProxy
from lxml import html
from fake_useragent import UserAgent
from random import randint
from time import sleep
import random
import requests
import json
import os


def pdf_generator(pdf_abstract, language):
    apd_url = "https://apd.usos.pwr.edu.pl"

    thesis_data[f"{language}_abstract"] = apd_url + pdf_abstract

    full_url = thesis_data[f"{language}_abstract"]

    try:
        # Delete comment to enable HTTP proxy
        #
        # response = requests.get(
        #     full_url,
        #     proxies=proxies,
        #     timeout=60,
        #     headers={"User-Agent": fake_ua, "Accept": "application/json"},
        # )
                
        response = requests.get(
            full_url,
            timeout=60,
            headers={"User-Agent": fake_ua, "Accept": "application/json"},
        )

        folder = f"pdf_abstracts/{language}"

        os.makedirs(folder, exist_ok=True)

        with open(f"{folder}/{language}_abstract_id_{thesis_id}.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
    except Exception as e:
        print(e)


thesis_No = 0

first_thesis_id = int(input("Input initial thesis id - minimum 1: "))
last_thesis_id = (
    int(input("Input final thesis id - maximum 16946 as of 26/08/2024: ")) + 1
)

ua = UserAgent()

# Delete comment to enable HTTP proxy
#
# proxy_list = []
#
# for proxy in range(5):
#     proxy = FreeProxy(rand=True, anonym=True, elite=True).get()
#     proxy_list.append(proxy)
#
# proxy = random.choice(proxy_list)

theses_list = []

current_directory = os.getcwd()

for thesis_id in range(first_thesis_id, last_thesis_id):
    url = f"https://apd.usos.pwr.edu.pl/diplomas/{thesis_id}"

    fake_ua = ua.random

    # Delete comment to enable HTTP proxy
    #
    # proxies = {"http": proxy, "https": proxy}

    try:
        # Delete comment to enable HTTP proxy
        #
        # response = requests.get(
        #     url,
        #     proxies=proxies,
        #     timeout=60,
        #     headers={"User-Agent": fake_ua, "Accept": "application/json"},
        # )

        response = requests.get(
            url,
            timeout=60,
            headers={"User-Agent": fake_ua, "Accept": "application/json"},
        )

        if response.status_code == 404:
            continue

        thesis_No += 1

        print(thesis_No, response)

        tree = html.fromstring(response.content)

        thesis_data = {
            "thesis_id": thesis_id,
            "thesis_type": " ".join(
                tree.xpath('//*[@id="pageBody"]/div/h1/span[2]/text()')
            ).strip(),
            "thesis_language": " ".join(
                tree.xpath('//*[@id="thesisInfo"]/tbody/tr[1]/td[2]/text()')
            ).strip(),
            "pl_title": " ".join(
                tree.xpath(
                    "//*[@id='thesisInfo']/tbody/tr[2]/td[2]/div/div[1]/div[2]/text()"
                )
            ).strip(),
            "en_title": " ".join(
                tree.xpath(
                    "//*[@id='thesisInfo']/tbody/tr[2]/td[2]/div/div[2]/div[2]/text()"
                )
            ).strip(),
        }

        pdf_pl_abstract = ""
        pdf_en_abstract = ""

        for tr_number in range(3, 12):
            thesis_information_field = " ".join(
                tree.xpath(f'//*[@id="thesisInfo"]/tbody/tr[{tr_number}]/td[1]/text()')
            ).strip()

            if thesis_information_field == "Promotor pracy:":
                thesis_data["thesis_promotor"] = " ".join(
                    tree.xpath(
                        f'//*[@id="thesisInfo"]/tbody/tr[{tr_number}]/td[2]/div/span/a/text()'
                    )
                ).strip()

            if thesis_information_field == "Jednostka organizacyjna:":
                thesis_data["faculty_id"] = " ".join(
                    tree.xpath(
                        f'//*[@id="thesisInfo"]/tbody/tr[{tr_number}]/td[2]/a/@data-fac_id'
                    )
                ).strip()

            if thesis_information_field == "Streszczenie:":
                thesis_data["pl_abstract"] = " ".join(
                    tree.xpath(
                        f"//*[@id='thesisInfo']/tbody/tr[{tr_number}]/td[2]/div/div[1]/div[2]/text()"
                    )
                ).strip()
                thesis_data["en_abstract"] = " ".join(
                    tree.xpath(
                        f"//*[@id='thesisInfo']/tbody/tr[{tr_number}]/td[2]/div/div[2]/div[2]/text()"
                    )
                ).strip()
                pdf_pl_abstract = " ".join(
                    tree.xpath(
                        f"//*[@id='thesisInfo']/tbody/tr[{tr_number}]/td[2]/div/div[1]/div[2]/a/@href"
                    )
                ).strip()
                pdf_en_abstract = " ".join(
                    tree.xpath(
                        f"//*[@id='thesisInfo']/tbody/tr[{tr_number}]/td[2]/div/div[2]/div[2]/a/@href"
                    )
                ).strip()

            if thesis_information_field == "Słowa kluczowe:":
                thesis_data["pl_keywords"] = " ".join(
                    tree.xpath(
                        f"//*[@id='thesisInfo']/tbody/tr[{tr_number}]/td[2]/div/div[1]/div[2]/text()"
                    )
                ).strip()
                thesis_data["en_keywords"] = " ".join(
                    tree.xpath(
                        f"//*[@id='thesisInfo']/tbody/tr[{tr_number}]/td[2]/div/div[2]/div[2]/text()"
                    )
                ).strip()

        if thesis_data["thesis_language"] == "angielski [EN]":
            thesis_data["pl_title"], thesis_data["en_title"] = (
                thesis_data["en_title"],
                thesis_data["pl_title"],
            )
            pdf_pl_abstract, pdf_en_abstract = pdf_en_abstract, pdf_pl_abstract
            thesis_data["pl_abstract"], thesis_data["en_abstract"] = (
                thesis_data["en_abstract"],
                thesis_data["pl_abstract"],
            )
            thesis_data["pl_keywords"], thesis_data["en_keywords"] = (
                thesis_data["en_keywords"],
                thesis_data["pl_keywords"],
            )

        if pdf_pl_abstract and pdf_en_abstract:
            pdf_generator(pdf_pl_abstract, "pl")
            pdf_generator(pdf_en_abstract, "en")

        theses_list.append(thesis_data)

        sleep(randint(1, 3))
    except Exception as e:
        print(e)

        # Delete comment to enable HTTP proxy
        #
        # proxy = random.choice(proxy_list)

if "usos-abstracts-scraper" in os.path.basename(current_directory):
    file_path = os.path.join(current_directory, "theses_data.json")
else:
    file_path = os.path.join(
        current_directory, "usos-abstracts-scraper", "theses_data.json"
    )

with open(file_path, "w") as file:
    json.dump(theses_list, file, indent=4, separators=(",", ": "))
