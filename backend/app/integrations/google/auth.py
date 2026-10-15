"""Google OAuth (read-only scopes).  One-time login:  python -m app.integrations.google.auth"""
from pathlib import Path
from app.config import settings

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]


def get_credentials():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    token = Path(settings.google_token_file)
    if not token.exists():
        raise RuntimeError("No token.json - run: python -m app.integrations.google.auth")
    creds = Credentials.from_authorized_user_file(str(token), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token.write_text(creds.to_json())
    return creds


def service(name: str, version: str):
    from googleapiclient.discovery import build
    return build(name, version, credentials=get_credentials(), cache_discovery=False)


def login() -> None:
    from google_auth_oauthlib.flow import InstalledAppFlow
    cfg = {"installed": {
        "client_id": settings.google_client_id, "client_secret": settings.google_client_secret,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"]}}
    creds = InstalledAppFlow.from_client_config(cfg, SCOPES).run_local_server(port=0)
    Path(settings.google_token_file).write_text(creds.to_json())
    print("Saved", settings.google_token_file)


if __name__ == "__main__":
    login()
