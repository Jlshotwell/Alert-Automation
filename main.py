import os.path
import sorting

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
  """
  This function authenticates to the 
  Google Cloud Platform using OAuth 2.0,
  reads system alerts and prints the devices
  generating alerts.
  """
  creds = None

  # Log in will be necessary for first time use
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Writes credentials to a JSON file for future authentication
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    
    # Call the Gmail API with REST
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=100, q='subject:Alert').execute()
    messages = results.get('messages', [])

    for message in messages:
      msg = service.users().messages().get(userId='me', id=message['id']).execute()
      email_data = msg['payload']['headers']
      subject = [i['value'] for i in email_data if i["name"]=="Subject"]
      for alert in subject:
        print(subject)
        for o_name in sorting.organizations:
          if o_name.name in alert:
            sorting.organization.system_filter(o_name, alert)
            
        
    #Print devices generating alerts
    for o in sorting.organizations:
        for device in o.devices:
          if device.memory > 5:
            print(o.name)
            device.report()
          elif device.storage > 1:
            print(o.name)
            device.report()
          elif device.disk_active:
            print(o.name)
            device.report()

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  sorting.sort_csv('ALL.csv')
  sorting.create_device_list('ALL.csv')
  main()


