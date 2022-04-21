import csv
import dataclasses
from datetime import date
import json
import pathlib
from urllib.parse import unquote
from typing import List, Dict, Optional

from lxml.html import document_fromstring, fromstring, HtmlElement
import requests

from .helpers import extract_latitude, extract_longitude, extract_status


@dataclasses.dataclass
class Certificate:

    id: str
    status: str
    holder: str
    scope: str
    materials: str
    valid_from: str
    valid_to: str
    body_short: str
    body_long: str
    latitude: float
    longitude: float
    certificate_url: str
    audit_url: str

    @classmethod
    def prepare_fieldnames(cls):
        return list(cls.__dataclass_fields__.keys())


def data_to_csv(data: List[Certificate], filename: str = 'iscc.csv'):
    """Save list with certificates to csv file."""
    pathlib.Path('data').mkdir(exist_ok=True)
    with open(pathlib.Path('data') / filename, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=Certificate.prepare_fieldnames())
        writer.writeheader()
        for cert in data:
            writer.writerow(dataclasses.asdict(cert))


def cert_dict_from_tablerow(tr: list) -> dict:
    """Take tablerow and prepare a dictionary representing one certificate.
    Find data, sometimes with xpath and clean them if necessary.
    """
    cert = {}

    xpath_map = {
        'id': (1, None),
        'status': (0, '//@title'),
        'holder': (2, '//@title'),
        'scope': (3, '//text()'),
        'materials': (4, '//@title'),  # sometimes can be accessed directly
        'valid_from': (7, None),
        'valid_to': (8, None),
        'body_short': (10, '//text()'),
        'body_long': (10, '//@title'),
        'latitude': (11, '//@href'),
        'longitude': (11, '//@href'),
        'certificate_url': (12, '//@href'),
        'audit_url': (13, '//@href'),
    }

    clean_map = {
        'status': extract_status,
        'latitude': extract_latitude,
        'longitude': extract_longitude,
        'certificate_url': str.strip,
        'audit_url': str.strip,
    }

    cert['status'] = 'valid'

    # Some elements has to be converted to HtmlElement, others are extracted directly
    # Materials can be extracted randomly in both ways
    # Sometimes data are missing (IndexError)
    for k, (index_, xpath_loc) in xpath_map.items():
        if tr[index_] is None:
            cert[k] = None
            continue
        try:
            if k == 'materials':  # materials are tricky
                materials = fromstring(tr[index_]).xpath(xpath_loc)
                if materials:
                    cert[k] = materials[0]
                else:
                    cert[k] = tr[index_]
            elif xpath_loc:
                cert[k] = fromstring(tr[index_]).xpath(xpath_loc)[0]
            else:
                cert[k] = tr[index_]
        except IndexError:
            cert[k] = None  # type: ignore

    # Process some of the values with functions in clean_map
    for k, v in cert.items():
        if (k in clean_map) and (v is not None):
            cert[k] = clean_map[k](v)

    return cert


def prepare_data(url, headers):
    """Prepare data for the post request for AJAX calls.

    Find wdtNonce value and update body of the post request.
    """
    r = requests.get(url, headers=headers)

    tree = document_fromstring(r.text)
    wdtnonce = tree.xpath('//*[@id="wdtNonceFrontendEdit_9"]/@value')[0] # valid are wdtNonceFrontendEdit_10

    # Copied from developer tools in the browser (Copy as cURL)
    percent_encoded_body = 'draw=2&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=cert_ikon&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=cert_number&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=cert_owner&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=cert_certified_as&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=cert_in_put&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=cert_add_on&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=cert_valid_from&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=cert_valid_until&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=cert_suspended_date&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=cert_issuer&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=cert_map&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=cert_file&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=12&columns%5B12%5D%5Bname%5D=cert_audit&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=7&order%5B0%5D%5Bdir%5D=desc&start=0&length=-1&search%5Bvalue%5D=&search%5Bregex%5D=false&wdtNonce=526e06d082&sRangeSeparator=%7C'

    body = unquote(percent_encoded_body)

    data = {k: v for k, v in (item.split('=') for item in body.split('&'))}
    # This key keeps changing. Update it before AJAX calls
    data['wdtNonce'] = wdtnonce

    return data


def main():
    # URL = 'https://www.iscc-system.org/certificates/valid-certificates/'
    URL = 'https://www.iscc-system.org/certificates/all-certificates/'

    XHR_URL = 'https://www.iscc-system.org/wp-admin/admin-ajax.php'

    HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 13982.88.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.162 Safari/537.36'
    }

    PARAMS = (
        ('action', 'get_wdtable'),
        ('table_id', '9'), # table_id value for valid is 10
    )

    # For subsequent AJAX call we need value of wdtNonce to update body of the post request
    data_for_post_request = prepare_data(URL, HEADERS)

    response = requests.post(
        XHR_URL, params=PARAMS, headers=HEADERS, data=data_for_post_request
    )

    # Parse response from AJAX call as JSON and access data attribute, which is list of rows from the table
    # Each row itself is a list of cells with data we need
    response_data = json.loads(response.text)['data']

    certificates = []

    for row in response_data:
        cert = Certificate(**cert_dict_from_tablerow(row))
        certificates.append(cert)

    data_to_csv(certificates)


if __name__ == '__main__':
    main()
