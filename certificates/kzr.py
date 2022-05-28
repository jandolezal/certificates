import csv
import json
import pathlib
from typing import List

import requests
from lxml.html import document_fromstring, HtmlElement, fromstring


KZR_BASE_URL = "http://certyfikaty.kzr.inig.eu/en"
KZR_POST_URL = "http://certyfikaty.kzr.inig.eu/table-part/en"
FIELDNAMES = ("status", "cert_num", "url", "company_num", "name", "address", "location", "valid_from", "valid_to", "scope", "body", "notes")


def process_table(table: HtmlElement) -> List[str]:
    trs = table.xpath("//table/tbody/tr")

    certs = []

    for tr in trs:
        cert = []
        
        tds = tr.findall("td")
        
        # Skip first column, second and third need individual treatment
        try:
            status = tds[1].find("span").attrib.get("title")
            # Encode status in English
            if "aktywny" in status:
                status = "active"
            elif "zawieszony" in status:
                status = "suspended"
            elif "wygasł" in status:
                status = "expired"

        # This is a page without a certificates
        except IndexError:
            return []
        num = tds[2].text.strip()

        try:
            url = tds[2].find("a").attrib.get("href")
        except AttributeError:
            url = ""
        cert.extend([status, num, url])

        # Rest of the columns handle in bulk (there are still two special cases)
        for td in tds[3:]:
            #special case with target text in divs: certification scope
            divs = td.findall("div")
            # special case with locations hidden in button title: location
            button = td.find("button")
            if divs:
                try:
                    cell_text = "|".join([scope.strip() for scope in td.text_content().split(";")])
                    # html elements are not consistent. ugly workaround for now
                    other_index = cell_text.find("Other")
                    cell_text = cell_text[:other_index] + "|" + cell_text[other_index:]
                except TypeError:
                    cell_text = ""
            elif button is not None:
                cell_text = button.attrib.get("title")
            else:
                cell_text = td.text

            # Clean values before appending to list
            if cell_text:
                cell = cell_text.strip()    
            else:
                cell = ""
            if cell == "---":
                cell = ""
            cell = cell.replace("\xa0", " ")
            cell = cell.replace("\r", "")
            cell = cell.replace("\n", "")
            cell = cell.replace("\t", "")

            cert.append(cell)

        certs.append(cert)

    return certs


def scrape_kzr():
    kzr_certs = []

    i = 1

    # Number of pages is not known ahead
    while True:
        print(f"Processing page: {i}")
        r = requests.post(KZR_POST_URL, data={"pageNum": i, "locale": "en"})
        table = fromstring(json.loads(r.text)["data"])
        certs = process_table(table)
        if not certs:
            break
        kzr_certs.extend(certs)
        i += 1

    with open(pathlib.Path("data") / "kzr.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDNAMES)
        writer.writerows(kzr_certs)


if __name__ == "__main__":
    scrape_kzr()
