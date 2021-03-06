# ISCC and KZR INiG certificates

Python modules for scraping published [ISCC](https://www.iscc-system.org/certificates/all-certificates/) and [KZR INiG](http://certyfikaty.kzr.inig.eu/en) certificates.

There is a Github Action which scrapes the certificates daily and takes advantage of Datasette to publish scraped certificates as SQLite database hosted by Heroku at [red-certificates](https://red-certificates.herokuapp.com/).

These certificates are issued by voluntary schemes based on the [Renewable Energy Directive (RED)](https://energy.ec.europa.eu/topics/renewable-energy/renewable-energy-directive-targets-and-rules/renewable-energy-directive_en), which operators in the bioenergy industry can use to certify the supply chain of bioenergy and related GHG emissions savings.

## Usage

```bash
# Prepare virtual environment and install dependencies

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

# Scrape certificates with requests and lxml and save them as .csv files to the data directory

python -m certificates.iscc

python -m certificates.kzr
```

Alternatively install basic CLI app using setup.py and pip

```bash
pip install .
certificates --help

Usage: certificates [OPTIONS]

  Scrape bioenergy sustainability certificates.

Options:
  --scheme [all|iscc|kzr]  Choose voluntary scheme to scrape (default: all)
  --help                   Show this message and exit.

```

## Description of the data

### ISCC

Scope abbreviations are listed on the [page](https://www.iscc-system.org/certificates/all-certificates/) below the table.

| Column | Description |
| ----------- | ----------- |
| status | Status of the certificate: valid, expired, withdrawn |
| id | Certificate ID |
| holder | Certificate holder |
| scope | Certification scope. Comma-separated abbreviations of the scopes |
| materials | Raw materials. Comma-separated strings |
| valid_from | Valid from |
| valid_to | Valid to |
| body_short | Certification body (abbreviation) |
| body_long | Certification body (name) |
| latitude | Latitude |
| longitude | Longitude |
| certificate_url | Certificate (link to pdf) |
| audit_url | Audit report (link to pdf) |

#### Scopes vocabulary

| Code | Description |
| ----------- | ----------- |
| BG | Biogas plant |
| BM | Biomethane plant |
| BP | Biodiesel plant |
| COF | Central Office (Group of farms/plantations) | 
| COP | Central Office (Group of Points of Origin) |
| CP | Collecting Point (for waste/residue material not grown/harvested on farms/plantations) |
| CPP | Co-Processing plant |
| CR | Crushing plant |
| EP | Ethanol plant |
| ET | ETBE plant |
| FA | Farm / Plantation |
| FG | First Gathering Point (for biomass grown/harvested on farms/plantations) |
| HVO | HVO plant |
| ISHC | Central Office for Independent Smallholders |
| LC | Logistic Center |
| LP | Liquefaction Plant |
| ML | Methanol plant |
| MP | Melting plant |
| MT | MTBE plant |
| OM | Oil mill | 
| OT | Other conversion unit |
| PM | Pulp mill |
| PO | Point of Origin |
| PP | Polymerization plant |
| PYP | Pyrolysis plant |
| RE | Refinery |
| SC | Steam cracking |
| SM | Sugar mill |
| TR | Trader |
| TRS | Trader with storage |
| TW | Treatment plant for waste/ residues |
| WH | Warehouses |


### KZR INiG

| Column | Description |
| ----------- | ----------- |
| status | Status of the certificate: active, expired, suspended |
| cert_num | Certificate number |
| url | Link to the certificate |
| company_num | Participant number |
| name | Name of the participant (company) |
| address | Address |
| location | Location |
| valid_from | Issued on |
| valid_to | Valid until |
| scope | Scope of the certification |
| body | Certification body |
| notes | Notices |


## TODO

Scrape [SURE](https://certification.sure-system.org/SearchVerifications) certificates.
