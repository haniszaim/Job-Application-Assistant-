import os
import gspread
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_PATH = BASE_DIR / "credentials" / "google_credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    creds =Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.getenv("SHEET_ID")).sheet1
    return sheet

def log_application(company, role, url,source,location, cover_letter_path, cv_version, status ="To apply" ):
    sheet = get_sheet()

    row =[
        str(date.today()),
        company,
        role,
        url,
        source,
        location,
        cover_letter_path,
        cv_version,
        "",
        status,
        "",
        ""
    ]

    sheet.append_row(row)
    print(f"Logged: {company}- {role}")