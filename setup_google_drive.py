#!/usr/bin/env python3
"""
Google Drive/Docs Integration Setup
Helps connect to Google Drive and Google Docs for file access
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required libraries are installed"""
    missing = []
    
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        print("✓ Google API libraries found")
        return True
    except ImportError:
        print("✗ Google API libraries not found")
        print("\nTo install:")
        print("  pip3 install --user google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        return False

def setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*80)
    print("GOOGLE DRIVE API SETUP INSTRUCTIONS")
    print("="*80)
    print("\n1. Go to Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    print("\n2. Create a new project (or select existing)")
    print("\n3. Enable APIs:")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Enable 'Google Drive API'")
    print("   - Enable 'Google Docs API'")
    print("\n4. Create OAuth Credentials:")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'OAuth client ID'")
    print("   - Application type: 'Desktop app'")
    print("   - Download the JSON file")
    print("   - Save as 'credentials.json' in this directory")
    print("\n5. Install Python libraries:")
    print("   pip3 install --user google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    print("\n6. Run this script again to authenticate")
    print("\n" + "="*80)

def create_download_script():
    """Create a script to download Google Docs"""
    script_content = '''#!/usr/bin/env python3
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
'''
    
    with open('download_google_docs.py', 'w') as f:
        f.write(script_content)
    print("\n✓ Created 'download_google_docs.py' script")

def main():
    """Main function"""
    print("Google Drive/Docs Integration Setup\n")
    
    if not check_dependencies():
        setup_instructions()
        create_download_script()
        return
    
    print("\n✓ All dependencies installed!")
    print("\nNext steps:")
    print("1. Follow setup instructions above to get credentials.json")
    print("2. Run: python3 download_google_docs.py <folder_id>")
    print("\nTo find a folder ID:")
    print("  - Open the folder in Google Drive")
    print("  - Look at the URL: .../folders/FOLDER_ID_HERE")
    print("  - Copy the FOLDER_ID_HERE part")

if __name__ == '__main__':
    main()
