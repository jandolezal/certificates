from datetime import date
import json
import pathlib

import pytest

from certificates.iscc import Certificate

def test_fromrow():
    with open(pathlib.Path('tests') / 'sample_response.txt') as f:
        response = f.readline()
        data = json.loads(response)['data']
        assert data

        cert = Certificate(
            id='EU-ISCC-Cert-US201-70601508',
            status='valid',
            holder='Shandong Aomeng Energy Technology Development Co.,Ltd, North of Linbo Road North Head, Laozhaozhuang Town , 252600  Linqing City, Liaocheng City, Shandong Province, China',
            scope='CP, TR',
            materials=None,
            valid_from='2022-04-26',
            valid_to='2023-04-25',
            body_short='SCS',
            body_long='SCS Global Services, Emeryville, United States',
            latitude=36.879846,
            longitude=115.778568,
            certificate_url=None,
            audit_url=None,
        )
        # Check first certificate in data
        assert cert == Certificate.from_tablerow(data[0])
