# ISCC certificates

Scrape [valid](https://www.iscc-system.org/certificates/valid-certificates/) ISCC certificates.

## Usage

Prepare the environment.

`python3 -m venv venv`

`source venv/bin/activate`

`python -m pip install --upgrade pip`

`python -m pip install -r requirements.txt`

Scrape valid certificates with requests and lxml.

`python -m certificates.iscc`

## Description of the data

Scope abbreviations are listed on the [page](https://www.iscc-system.org/certificates/all-certificates/) below the table.

| Name | Description |
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
| downloaded | Date of the data download |


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
