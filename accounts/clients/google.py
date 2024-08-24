import requests
from typing import TypedDict
from django.conf import settings


class GoogleTokenResponse(TypedDict):
    access_token: str
    expires_in: int
    scope: str
    token_type: str
    id_token: str


class GoogleUserInfoResponse(TypedDict):
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str


class GoogleClient:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.grant_type = 'authorization_code'

        self.token_url = 'https://oauth2.googleapis.com/token'
        self.user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'

    def get_token(self, code: str) -> GoogleTokenResponse:
        """Documentation
        - https://developers.google.com/identity/protocols/oauth2/web-server?hl=ko#exchange-authorization-code
        """
        response = requests.post(
            url=self.token_url,
            data={
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
                'grant_type': self.grant_type,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token: str) -> GoogleUserInfoResponse:
        """Documentation
        - https://developers.google.com/identity/protocols/oauth2/openid-connect
        """
        response = requests.get(
            url=self.user_info_url,
            params={'access_token': access_token},
        )
        response.raise_for_status()
        return response.json()
