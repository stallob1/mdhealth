#!/usr/bin/env python3
"""
Download Google Docs from a Drive folder
"""
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """Authenticate with Google Drive"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def download_docs_from_folder(folder_id, output_dir='google_docs'):
    """Download all Google Docs from a folder"""
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # List files in folder
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.document'",
        fields="files(id, name)"
    ).execute()
    
    files = results.get('files', [])
    print(f"Found {len(files)} Google Docs")
    
    for file in files:
        print(f"Downloading: {file['name']}")
        request = service.files().export_media(
            fileId=file['id'],
            mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
        output_path = os.path.join(output_dir, f"{file['name']}.docx")
        with open(output_path, 'wb') as f:
            f.write(request.execute())
        print(f"  ✓ Saved to {output_path}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 download_google_docs.py <folder_id>")
        print("To find folder ID: Open folder in Google Drive, ID is in URL")
        sys.exit(1)
    
    folder_id = sys.argv[1]
    download_docs_from_folder(folder_id)
