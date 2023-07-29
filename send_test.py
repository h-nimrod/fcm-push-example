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
  print(get_access_token(PRIVATE_KEY_JSON))
