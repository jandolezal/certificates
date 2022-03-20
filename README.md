# ISCC and KZR INiG certificates

Scrape valid [ISCC](https://www.iscc-system.org/certificates/valid-certificates/) and issued [KZR INiG](http://certyfikaty.kzr.inig.eu/en) certificates.

## Usage

Prepare the environment.

`python3 -m venv venv`

`source venv/bin/activate`

`python -m pip install --upgrade pip`

`python -m pip install -r requirements.txt`

Scrape certificates with requests and lxml.

`python -m certificates.iscc`

`python -m certificates.kzr`

## Description of the data

### ISCC

Scope abbreviations are listed on the [page](https://www.iscc-system.org/certificates/all-certificates/) below the table.

| Column | Description |
| ----------- | ----------- |
| status | Status of the certificate: valid |
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

## Scopes vocabulary

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
| status | Status (active, expired) |
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
