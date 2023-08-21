import argparse
from oauth2client.service_account import ServiceAccountCredentials

PRIVATE_KEY_JSON = 'sample-app-firebase-adminsdk-foobar.json' ### modify to match your environment
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

def get_access_token(private_key_json):
  """Retrieve a valid access token that can be used to authorize requests.                                                                                        

  :return: Access token.                                                                                                                                            """

  credentials = ServiceAccountCredentials.from_json_keyfile_name(private_key_json, SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--private-key-json-file', help="give private key json file")
  args = parser.parse_args()

  private_key_json = PRIVATE_KEY_JSON
  if args.private_key_json_file:
    private_key_json = args.private_key_json_file
    

  print(get_access_token(args.private_key_json_file))
