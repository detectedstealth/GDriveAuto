import argparse
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


def create_parser():
  parser = argparse.ArgumentParser(description="Command-line Google APIs")
  parser.add_argument("-f", "--folder", metavar="", help="Create new Google Drive folder")
  return parser

def authenticate():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds

def find_folder(service, folder_name):
  """Find a folder by name in Google Drive."""
  try:
    # Use the Drive API to list files with the specified folder name
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    results = (
      service.files()
      .list(q=query, spaces="drive", fields="files(id, name)")
      .execute()
    )
    items = results.get("files", [])

    if not items:
      print(f"Folder '{folder_name}' does not exist.")
      return None

    print(f"Folder '{folder_name}' exists:")
    for item in items:
      print(f"Name: {item['name']}, ID: {item['id']}")
    return items  # Returns the list of matching folders

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None


def main(folder_name="ProjectFolder"):
  """Drive v3 API.
  Creates a folder in Google Drive, if it does not exist already.
  """
  creds = None
  creds = authenticate()

  try:
    service = build("drive", "v3", credentials=creds)

    # Check if the drive folder already exists
    found_folders = find_folder(service, folder_name)
    if found_folders is not None:
      print(f"Folder '{folder_name}' already exists.")
      return

    # Call the Drive v3 API.
    file_metadata = {
      "name": folder_name,
      "mimeType": "application/vnd.google-apps.folder"
    }
    results_folder = (
      service.files().create(body=file_metadata, fields="id").execute()
    )
    print(f"Created Folder ID: {results_folder.get('id')} name: {folder_name}")

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  parser = create_parser()
  args = parser.parse_args()

  if args.folder:
    main(args.folder)
  else:
    main()