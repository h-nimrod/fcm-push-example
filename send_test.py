import argparse
import json
from oauth2client.service_account import ServiceAccountCredentials

PRIVATE_KEY_JSON = 'sample-app-firebase-adminsdk-foobar.json' ### modify to match your environment
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

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--private-key-json-file', help="give private key json file")
  args = parser.parse_args()

  private_key_json = PRIVATE_KEY_JSON
  if args.private_key_json_file:
    private_key_json = args.private_key_json_file
    

  print(get_access_token(private_key_json))
