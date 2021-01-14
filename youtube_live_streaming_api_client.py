#!/usr/bin/env python3

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


class YoutubeLiveStreamingApiClient():

    def __init__(self, client_secrets_file, scopes):
        self.__client = self.get_authenticated_service(
            client_secrets_file, scopes)

    def get_authenticated_service(self, client_secrets_file, scopes):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file, scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    def get_live_chat_id(self, live_id):
        live_broadcasts = self.__client.liveBroadcasts().list(
            part='snippet', id=live_id, fields='items(snippet(liveChatId))').execute()

        return live_broadcasts['items'][0]['snippet']['liveChatId']

    def send_message_to_live_chat(self, live_chat_id, message):
        self.__client.liveChatMessages().insert(part='snippet', body={
            'snippet': {
                'liveChatId': live_chat_id,
                'type': 'textMessageEvent',
                'textMessageDetails': {
                    'messageText': message
                }
            }
        }).execute()
