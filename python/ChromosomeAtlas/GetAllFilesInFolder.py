import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
CREDENTIALS_FILE = "client_secret_563563514748-486lji2ouvg2svb016j2gbe65135ks9r.apps.googleusercontent.com.json"


def print_files_in_folder(service, folder_id):
    kwargs = {
        "q": "'{}' in parents".format(folder_id),
        # Specify what you want in the response as a best practice. This string
        # will only get the files' ids, names, and the ids of any folders that they are in
        "fields": "nextPageToken,incompleteSearch,files(id,parents,name)",
        # Add any other arguments to pass to list()
    }
    request = service.files().list(**kwargs)
    all_files = {}
    while request is not None:
        response = request.execute()
        # Do stuff with response['files']
        for f in response["files"]:
            name = f["name"]
            name = re.sub(r"[^A-Za-z]", "", name)
            all_files[name] = f["id"]
        request = service.files().list_next(request, response)

    for fname in sorted(list(all_files.keys())):
        print(f'"{fname}": ["{all_files[fname]}", True],')


if __name__ == "__main__":
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)
    print_files_in_folder(service, "1lnRsMqKXjyX7DaWA1Yjr1ca5pFXTJtdJ")
