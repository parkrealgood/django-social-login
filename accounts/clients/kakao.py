from typing import TypedDict

import requests
from django.conf import settings


class KakaoTokenResponse(TypedDict):
    token_type: str
    access_token: str
    id_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    scope: str


class KakaoProfileResponse(TypedDict):
    nickname: str


class KakaoAccountResponse(TypedDict):
    profile_needs_agreement: bool
    profile_nickname_needs_agreement: bool
    profile: KakaoProfileResponse


class KakaoUserInfoResponse(TypedDict):
    id: int
    connected_at: str
    kakao_account: KakaoAccountResponse


class KakaoClient:
    """Documentation
    - https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#kakaologin
    """
    def __init__(self):
        self.grant_type = 'authorization_code'
        self.client_id = settings.KAKAO_CLIENT_ID
        self.redirect_uri = settings.KAKAO_REDIRECT_URI

        self.token_url = 'https://kauth.kakao.com/oauth/token'
        self.user_info_url = 'https://kapi.kakao.com/v2/user/me'

    def get_token(self, code: str) -> KakaoTokenResponse:
        response = requests.post(
            url=self.token_url,
            headers={
                'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
            },
            data={
                'grant_type': self.grant_type,
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'code': code,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token: str) -> KakaoUserInfoResponse:
        response = requests.post(
            url=self.user_info_url,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
            },
        )
        response.raise_for_status()
        return response.json()
