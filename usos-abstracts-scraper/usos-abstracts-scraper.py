import aiohttp
import asyncio
from lxml import html
from fake_useragent import UserAgent
import json
import os
from tenacity import retry, stop_after_attempt, wait_exponential
import aiofiles


async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.text()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_thesis_data(session, thesis_id, ua):
    url = f"https://apd.usos.pwr.edu.pl/diplomas/{thesis_id}"
    fake_ua = ua.random
    headers = {"User-Agent": fake_ua, "Accept": "application/json"}

    try:
        content = await fetch(session, url, headers)
    except aiohttp.ClientResponseError as e:
        if e.status == 404:
            return None
        raise

    tree = html.fromstring(content)

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
        await pdf_generator(session, pdf_pl_abstract, "pl", thesis_data, thesis_id)
        await pdf_generator(session, pdf_en_abstract, "en", thesis_data, thesis_id)

    return thesis_data


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def pdf_generator(session, pdf_abstract, language, thesis_data, thesis_id):
    apd_url = "https://apd.usos.pwr.edu.pl"
    thesis_data[f"{language}_abstract"] = apd_url + pdf_abstract
    full_url = thesis_data[f"{language}_abstract"]

    headers = {"User-Agent": UserAgent().random, "Accept": "application/json"}
    async with session.get(full_url, headers=headers) as response:
        content = await response.read()

    folder = f"pdf_abstracts/{language}"
    os.makedirs(folder, exist_ok=True)

    async with aiofiles.open(
        f"{folder}/{language}_abstract_id_{thesis_id}.pdf", "wb"
    ) as pdf_file:
        await pdf_file.write(content)


async def process_theses(first_thesis_id, last_thesis_id):
    ua = UserAgent()
    theses_list = []
    semaphore = asyncio.Semaphore(40)  # Limit to 40 concurrent requests

    async def fetch_with_semaphore(session, thesis_id):
        async with semaphore:
            return await fetch_thesis_data(session, thesis_id, ua)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for thesis_id in range(first_thesis_id, last_thesis_id):
            task = asyncio.ensure_future(fetch_with_semaphore(session, thesis_id))
            tasks.append(task)

        for task in asyncio.as_completed(tasks):
            try:
                thesis_data = await task
                if thesis_data:
                    theses_list.append(thesis_data)
                    print(f"Processed thesis {thesis_data['thesis_id']}")
            except Exception as exc:
                print(f"Thesis generated an exception: {exc}")

    return theses_list


async def main():
    first_thesis_id = int(input("Input initial thesis id - minimum 1: "))
    last_thesis_id = (
        int(input("Input final thesis id - maximum 16946 as of 26/08/2024: ")) + 1
    )

    theses_list = await process_theses(first_thesis_id, last_thesis_id)

    current_directory = os.getcwd()
    if "usos-abstracts-scraper" in os.path.basename(current_directory):
        file_path = os.path.join(current_directory, "theses_data.json")
    else:
        file_path = os.path.join(
            current_directory, "usos-abstracts-scraper", "theses_data.json"
        )

    async with aiofiles.open(file_path, "w") as file:
        await file.write(json.dumps(theses_list, indent=4, separators=(",", ": ")))


if __name__ == "__main__":
    asyncio.run(main())
