#!/usr/bin/env python3

import urllib.parse

from youtube_live_streaming_api_client import YoutubeLiveStreamingApiClient

YOUTUBE_CLIENT_SECRETS_FILE = 'client_secrets.json'
YOUTUBE_CLIENT_SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl']


def main():
    youtube = YoutubeLiveStreamingApiClient(
        YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_CLIENT_SCOPES)

    url = input('YouTube Live URL: ')
    live_id = urllib.parse.urlparse(url).path[1:]
    live_chat_id = youtube.get_live_chat_id(live_id)

    youtube.send_message_to_live_chat(live_chat_id, '[test]')


if __name__ == '__main__':
    main()
