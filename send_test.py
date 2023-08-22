import argparse
import json
import requests
from oauth2client.service_account import ServiceAccountCredentials

PRIVATE_KEY_JSON = 'sample-app-firebase-adminsdk-foobar.json' ### modify to match your environment
DEFAULT_MESSAGE_JSON = 'sample_message.json'
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

def get_access_token(private_key_json):
  """
  Retrieve a valid access token that can be used to authorize requests.

  Parameter:
  - private_key_json (str): Path to the JSON file containing the service account's private key.

  Returns: Access token (str).
  """

  credentials = ServiceAccountCredentials.from_json_keyfile_name(private_key_json, SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token

def get_message_json(target_device_token, template_json_file):
  """
  Load a message template from a JSON file and set the target device token.

  Parameters:
  - target_device_token (str): The token of the target device.
  - template_json_file (str, optional): Path to the JSON file that contains the message template. Defaults to 'sample_message.json'.

  Returns:
  - dict: A dictionary representing the loaded message template, with the token set to the provided target device token.
  """

  with open(template_json_file, 'r', encoding='utf-8') as file:
    obj = json.load(file)

  if target_device_token != None:
    obj["message"]["token"] = target_device_token

  return obj

def get_project_id_from_json(private_key_json_file):
  """
  Retrieve the project ID from a given private key JSON file.

  Parameters:
  - private_key_json (str): Path to the JSON file that contains the private key information.

  Returns:
  - str: The project ID extracted from the JSON file.
  """

  with open(private_key_json_file, 'r', encoding='utf-8') as file:
    obj = json.load(file)

  return obj["project_id"]

def send_push_message(access_token, device_token, private_key_json_file=PRIVATE_KEY_JSON, message_json_file=DEFAULT_MESSAGE_JSON):
  """
  Send a push notification via Firebase Cloud Messaging (FCM).

  This method sends a push notification to a specific device using FCM.
  The content of the notification is based on the provided JSON template file.
  If no template is provided, a default one is used. The project ID necessary for the FCM
  request is derived from a provided private key JSON file, or a default if none is given.

  Parameters:
  - access_token (str): The access token used for authentication with the FCM service.
  - device_token (str): The unique token of the target device to which the notification should be sent.
  - private_key_json_file (str, optional): The path to a JSON file containing the private key
    information used to derive the project ID. Defaults to PRIVATE_KEY_JSON.
  - message_json_file (str, optional): The path to a JSON file containing the message template
    for the notification. Defaults to DEFAULT_MESSAGE_JSON.
  """

  project_id = get_project_id_from_json(private_key_json_file)
  url = f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send'

  headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json; UTF-8',
  }

  message = get_message_json(target_device_token=device_token, template_json_file=message_json_file)

  print("=== Request ===")
  # print("Request headers: ", json.dumps(headers, indent=4, ensure_ascii=False))
  print("Request message: ", json.dumps(message, indent=4, ensure_ascii=False))

  response = requests.post(url, headers=headers, data=json.dumps(message))

  print("")
  print("=== Response ===")
  print("Response status code: ", response.status_code)
  print("Response content: ", response.text)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--private-key-json-file', help="give private key json file")
  args = parser.parse_args()

  private_key_json = PRIVATE_KEY_JSON
  if args.private_key_json_file:
    private_key_json = args.private_key_json_file
    

  print(get_access_token(private_key_json))
