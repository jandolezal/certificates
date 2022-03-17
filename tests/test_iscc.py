from datetime import date
import json
import pathlib

import pytest

from certificates.iscc import Certificate, cert_dict_from_tablerow

def test_fromrow():
    with open(pathlib.Path('tests') / 'sample_response.txt') as f:
        response = f.readline()
        data = json.loads(response)['data']
        assert data

        cert = Certificate(
            id='EU-ISCC-Cert-US201-70601157',
            status='valid',
            holder='UPM-Kymmene Inc., Shuman Boulevard 55, suite 400, 60563 Naperville, IL, United States',
            scope='CP, TRS',
            materials='CTO',
            valid_from='2021-09-17',
            valid_to='2022-09-16',
            body_short='SCS',
            body_long='SCS Global Services, Emeryville, United States',
            latitude=41.80511,
            longitude=-88.144217,
            certificate_url='https://certificates.iscc-system.org/cert-pdf/EU-ISCC-Cert-US201-70601157.pdf',
            audit_url='https://certificates.iscc-system.org/cert-audit/EU-ISCC-Cert-US201-70601157_audit.pdf',
        )
        # Check first certificate in data
        assert cert == Certificate(**cert_dict_from_tablerow(data[0]))
