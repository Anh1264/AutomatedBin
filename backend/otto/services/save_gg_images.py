from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from decouple import config
import json
import base64
import io

# SCOPES = ['https://www.googleapis.com/auth/drive.file']
def get_drive_service():
    """Authenticate and return the Google Drive API service."""
    creds = get_credentials_from_env()
    print("Creds:", creds)
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive(file_io, file_name, folder_name):
    service = get_drive_service()
    folder_id = get_or_create_folder(service, folder_name)
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
    items = results.get('files', [])

    if items:
        # File already exists, return the link to the existing file
        file_id = items[0]['id']
        return f"https://drive.google.com/uc?id={file_id}"
    file_metadata = {'name': file_name, 'parents': folder_id, }
    media = MediaIoBaseUpload(file_io, mimetype='image/jpeg', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    print('file_id:' ,file_id)
    permission =  {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file_id, body=permission).execute()
    return f"https://drive.google.com/uc?id={file_id}"
    # return f"https://drive.google.com/thumbnail?id={file['id']}&sz=w1000"

def get_or_create_folder(service, folder_name):
    print('folder name: ', folder_name)
    """Get the folder ID by name, or create it if it doesn't exist."""
    # Search for the folder
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])

    if items:
        # Folder exists
        print('Folder id:', items[0]['id'])
        return items[0]['id']
    else:
        # Create new folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print('Folder id:', folder['id'])
        return folder['id']
    

def get_credentials_from_env():
    print("Getting creds")
    encoded_creds = config('GOOGLE_CREDENTIALS_KEY')
    if not encoded_creds:
        raise ValueError("No GOOGLE_CREDENTIALS_KEY environment variable set")
    encoded_creds = str(encoded_creds)[2:]
    encoded_creds += "=="
    # print("encoded creds:", encoded_creds, "length:", len(encoded_creds))
    decoded_creds = json.loads(base64.b64decode(encoded_creds).decode('utf-8'))
    # print("Decoded creds:",decoded_creds)
    print("Load successful")
    credentials = service_account.Credentials.from_service_account_info(decoded_creds)
    return credentials    

def get_drive_link(b64_image_data, file_name, folder_name):
    file_data = base64.b64decode(b64_image_data)
    file_io = io.BytesIO(file_data)
    link = upload_file_to_drive(file_io, file_name, folder_name)
    print('link:', link)
    return link

# base_64_string = "string"
# file_name = "supposed to be inference ID"
# robot_id = "robotID"
# print('robot_id:', robot_id)
# drive_link = get_drive_link(base_64_string, file_name, robot_id)
# print('Drive Link:' ,drive_link)


