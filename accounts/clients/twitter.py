import base64
import requests
from typing import TypedDict
from urllib.parse import quote

from django.conf import settings


class TwitterTokenResponse(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
    scope: str
    token_type: str


class TwitterUserInfoDataResponse(TypedDict):
    id: str
    name: str
    username: str


class TwitterUserInfoResponse(TypedDict):
    data: TwitterUserInfoDataResponse


class TwitterClient:
    def __init__(self):
        self.grant_type = 'authorization_code'
        self.client_id = settings.TWITTER_CLIENT_ID
        self.client_secret = settings.TWITTER_CLIENT_SECRET
        self.redirect_uri = settings.TWITTER_OAUTH2_REDIRECT_URI
        self.code_verifier = 'challenge'

        self.token_url = 'https://api.x.com/2/oauth2/token'
        self.user_info = 'https://api.twitter.com/2/users/me'

    def _encode_rfc1738(self) -> (str, str):
        encoded_api_key = quote(self.client_id, safe='')
        encoded_api_secret = quote(self.client_secret, safe='')

        return encoded_api_key, encoded_api_secret

    def _get_credentials(self) -> str:
        encoded_api_key, encoded_api_secret = self._encode_rfc1738()
        credentials = f'{encoded_api_key}:{encoded_api_secret}'
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return f'Basic {encoded_credentials}'

    def get_token(self, code: str) -> TwitterTokenResponse:
        response = requests.post(
            url=self.token_url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data={
                'code': code,
                'grant_type': self.grant_type,
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'code_verifier': self.code_verifier,
            }
        )
        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token: str) -> TwitterUserInfoResponse:
        response = requests.get(
            url=self.user_info,
            headers={
                'Authorization': f'Bearer {access_token}'
            },
            params={
                'user.fields': 'id,username'
            }
        )
        response.raise_for_status()
        return response.json()
