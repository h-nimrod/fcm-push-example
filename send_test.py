"""
Module for sending push notifications via Firebase Cloud Messaging (FCM).
"""

import argparse
import json
import requests
from oauth2client.service_account import ServiceAccountCredentials

PRIVATE_KEY_JSON_DEFAULT = 'sample-app-firebase-adminsdk-foobar.json'
DEFAULT_MESSAGE_JSON = 'sample_message.json'
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


# pylint: disable=too-few-public-methods
class PushMessageArgs:
    """
    A class to encapsulate the arguments required for sending a push message.
    """

    def __init__(self, **kwargs):
        self.token = kwargs.get('token')
        self.device_token = kwargs.get('device_token')
        self.private_key_path = kwargs.get('private_key_path', PRIVATE_KEY_JSON_DEFAULT)
        self.message_json_path = kwargs.get('message_json_path', DEFAULT_MESSAGE_JSON)
        self.title = kwargs.get('title')
        self.body = kwargs.get('body')
        self.image = kwargs.get('image')

def get_access_token(private_key_path):
    """
    Retrieve a valid access token that can be used to authorize requests.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(private_key_path, SCOPES)
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token


def get_message_json(
        target_token,
        template_json_file=DEFAULT_MESSAGE_JSON,
        title_str=None,
        body_str=None,
        image_url=None
):
    """
    Load a message template from a JSON file and set the target device token.
    """
    with open(template_json_file, 'r', encoding='utf-8') as file:
        obj = json.load(file)

    if target_token:
        obj["message"]["token"] = target_token

    if title_str:
        obj["message"]["notification"]["title"] = title_str

    if body_str:
        obj["message"]["notification"]["body"] = body_str

    if image_url:
        obj["message"]["notification"]["image"] = image_url

    return obj


def get_project_id_from_json(private_key_path):
    """
    Retrieve the project ID from a given private key JSON file.
    """
    with open(private_key_path, 'r', encoding='utf-8') as file:
        obj = json.load(file)

    return obj["project_id"]


def send_push_message(push_args):
    """
    Send a push notification via Firebase Cloud Messaging (FCM).
    """
    project_id = get_project_id_from_json(args.private_key_path)
    url = f'https://fcm.googleapis.com/v1/projects/{project_id}/messages:send'

    headers = {
        'Authorization': f'Bearer {push_args.token}',
        'Content-Type': 'application/json; UTF-8',
    }

    message = get_message_json(
        target_token=push_args.device_token,
        template_json_file=push_args.message_json_path,
        title_str=push_args.title,
        body_str=push_args.body,
        image_url=push_args.image
    )

    print("=== Request ===")
    print("Request message: ", json.dumps(message, indent=4, ensure_ascii=False))

    response = requests.post(url, headers=headers, data=json.dumps(message), timeout=(10.0, 10.0))

    print("\n=== Response ===")
    print("Response status code: ", response.status_code)
    print("Response content: ", response.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device-token', help="give taget device token")
    parser.add_argument('-p', '--private-key-path',
                        help="give private key json file", default=PRIVATE_KEY_JSON_DEFAULT)
    parser.add_argument('-m', '--message-json',
                        help="give message json", default=DEFAULT_MESSAGE_JSON)
    parser.add_argument('-t', '--title', help="give title", default=None)
    parser.add_argument('-b', '--body', help="give body", default=None)
    parser.add_argument('-i', '--image', help="give image url", default=None)
    parser.add_argument('--print-access-token', action='store_true', help="print access token")
    args = parser.parse_args()

    access_token = get_access_token(args.private_key_path)

    if args.print_access_token:
        print("=== access token ===")
        print(access_token)
        print("")

    push_args_obj = PushMessageArgs(
        token=access_token,
        device_token=args.device_token,
        private_key_path=args.private_key_path,
        message_json_path=args.message_json,
        title=args.title,
        body=args.body,
        image=args.image
    )

    send_push_message(push_args_obj)
