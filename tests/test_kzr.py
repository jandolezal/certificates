import pathlib

from lxml.html import document_fromstring
import pytest

from certificates.kzr import process_table


def test_process_table():
    with open(pathlib.Path("tests") / "KZR INiG System - Issued Certificates.html") as f:
        table = document_fromstring(f.read())
        assert table is not None
        
        certs = process_table(table)
        assert len(certs) == 10
        first = [
            "active",
            "BVC/KZR/027/22",
            "http://certyfikaty.kzr.inig.eu/public/certs/2936.pdf",
            "81/7999/DD/14",
            "GRUPA LOTOS S.A.",
            "Polska, 80-718 Gdańsk, ul. Elbląska 135",
            "1.Polska, 80-718 Gdańsk, Ul. Elbląska 135; 2.  LOTOS Biopaliwa, Polska, 43-502 Czechowice-Dziedzice, ul. Łukasiewicza 2; 3. LOTOS Terminale, Polska, 43-502 Czechowice Dziedzice, ul Łukasiewicza 2; 4. Polska, 43-100 Tychy, ul. Przemysłowa 64; 5. Baltchem, Polska, 70-605 Szczecin, ul. Księdza Stanisława Kujota Nr 9;",
            "2022-03-19",
            "2023-03-18",
            "Trading with storage; Final supplierOther : Blending with conventional fuels and placing on the market",
            "Bureau Veritas Polska Sp. z o. o.",
            "",
            ]
        
        assert certs[0] == first

        assert certs[-1][3] == "1404/7999/DD/22"
