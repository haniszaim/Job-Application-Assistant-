import os 
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_PATH = BASE_DIR / "credentials" / "gmail_credentials.json"
TOKEN_PATH = BASE_DIR / "credentials" / "gmail_token.json"

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

def get_gmail_service():
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)

def create_draft(to_email, subject, email_body, pdf_path):
    service = get_gmail_service()

    message = MIMEMultipart()
    message["to"] = to_email
    message["subject"] = subject

    message.attach(MIMEText(email_body, "plain"))

    with open(pdf_path, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            f"attachment; filename=cover_letter.pdf"
        )
        message.attach(attachment)
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    draft = service.users().drafts().create(
        userId="me",
        body={"message":{"raw": raw}}
    ).execute()

    print(f"Draft created:{draft['id']}")
    return draft["id"]