# ChromosomeAtlas
Chromosome Atlas of Nepal -- Database and Book

# Python scripts to compile book

## Dependencies
``pip3 install google-api-python-client``

``pip3 install oauth2client``

## How to Run
Get credentials from Google API as described here: https://developers.google.com/identity/protocols/oauth2, and download the credentials file. When running the following command for the first time, you will need to login which creates a token.json file.

``python3 -m ChromosomeAtlas.LatexGenerator``

## 2020-Nov-23
- Working on reviving scripts and testing

# Meeting Notes
## 2018-Sep-19

- sent github invites
- Projects (1) BibTeX drafts, (2) Review, (3) Database Schema
- Created MySQL project in SQLdbm (completed first version of Schema)
- Explained the project high-level to Suraj
- Created Google Sheets for Acanthaceae and Aceraceae

# Schema

![alt text](DataBaseSchemaVersion1.png)
