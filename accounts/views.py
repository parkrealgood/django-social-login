import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.clients.google import GoogleClient
from accounts.clients.kakao import KakaoClient
from accounts.clients.twitter import TwitterClient
from accounts.constants import (
    GOOGLE_ACCOUNT_URL, KAKAO_AUTHORIZE_URL, TWITTER_REQUEST_TOKEN_URL, TWITTER_AUTHORIZE_URL, TWITTER_ACCESS_TOKEN_URL,
    TWITTER_OAUTH2_AUTHORIZE_URL
)
from accounts.utils import get_oauth1_session


class GoogleLoginView(APIView):
    """Google 로그인 페이지로 리디렉션"""
    def get(self, request):
        """
        Documentation : https://developers.google.com/identity/protocols/oauth2/web-server?hl=ko#sample-oauth-2.0-server-response
        """
        google_base_url = GOOGLE_ACCOUNT_URL
        scope = 'email profile'
        google_auth_url = (
            f'{google_base_url}'
            f'&client_id={settings.GOOGLE_CLIENT_ID}'
            f'&redirect_uri={settings.GOOGLE_REDIRECT_URI}'
            f'&scope={scope}'
        )
        return redirect(google_auth_url)


class GoogleCallbackView(APIView):
    """Google로부터 리디렉션 받은 후 처리"""
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        token = GoogleClient().get_token(code=code)
        access_token = token.get('access_token')
        if not access_token:
            return Response({'error': 'access_token is required'}, status=status.HTTP_400_BAD_REQUEST)
        user_info = GoogleClient().get_user_info(access_token=access_token)
        if not user_info:
            return Response({'error': 'user_info is required'}, status=status.HTTP_400_BAD_REQUEST)

        email = user_info.get('email')

        return Response({'message': f'{email} login success'}, status=status.HTTP_200_OK)


class KakaoLoginView(APIView):
    """Kakao 로그인 페이지"""
    def get(self, request):
        client_id = settings.KAKAO_CLIENT_ID
        redirect_uri = settings.KAKAO_REDIRECT_URI
        kakao_oauth_url = (f'{KAKAO_AUTHORIZE_URL}'
                           f'?client_id={client_id}'
                           f'&redirect_uri={redirect_uri}'
                           f'&response_type=code'
                           f'&prompt=none')
        return redirect(kakao_oauth_url)


class KaKaoCallbackView(APIView):
    """Kakao로부터 리디렉션 받은 후 처리"""
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        token = KakaoClient().get_token(code=code)
        if not token:
            return Response({'error': 'token is required'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token.get('access_token')
        if not access_token:
            return Response({'error': 'access_token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = KakaoClient().get_user_info(access_token=access_token)
        user_nickname = user_info.get('kakao_account').get('profile').get('nickname')
        return Response({'message': f'{user_nickname} login success'}, status=status.HTTP_200_OK)


class TwitterLoginView(APIView):
    """Twitter 로그인 페이지"""
    def get(self, request):
        oauth = get_oauth1_session(
            client_key=settings.TWITTER_API_KEY,
            client_secret=settings.TWITTER_API_SECRET_KEY,
            callback_uri=settings.TWITTER_OAUTH1_REDIRECT_URI
        )

        try:
            fetch_response = oauth.fetch_request_token(url=TWITTER_REQUEST_TOKEN_URL)
            request.session['oauth_token'] = fetch_response.get('oauth_token')
            request.session['oauth_token_secret'] = fetch_response.get('oauth_token_secret')

            # 사용자를 트위터 로그인 페이지로 리디렉션
            authorization_url = oauth.authorization_url(url=TWITTER_AUTHORIZE_URL)
            return redirect(to=authorization_url)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TwitterCallbackView(APIView):
    """Twitter로부터 리디렉션 받은 후 처리"""
    def get(self, request):
        oauth_token = request.session.get('oauth_token')
        oauth_token_secret = request.session.get('oauth_token_secret')
        oauth_verifier = request.GET.get('oauth_verifier')

        oauth = get_oauth1_session(
            client_key=settings.TWITTER_API_KEY,
            client_secret=settings.TWITTER_API_SECRET_KEY,
            resource_owner_key=oauth_token,
            resource_owner_secret=oauth_token_secret,
            verifier=oauth_verifier
        )

        try:
            oauth_tokens = oauth.fetch_access_token(url=TWITTER_ACCESS_TOKEN_URL)
            request.session['access_token'] = oauth_tokens.get('oauth_token')
            request.session['access_token_secret'] = oauth_tokens.get('oauth_token_secret')

            # 성공 페이지 렌더링
            return Response({'message': f'twitter login success'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TwitterOauth2LoginView(APIView):
    """Twitter 로그인 페이지"""
    def get(self, request):
        authorization_url = TWITTER_OAUTH2_AUTHORIZE_URL
        params = {
            'response_type': 'code',
            'client_id': settings.TWITTER_CLIENT_ID,
            'redirect_uri': settings.TWITTER_OAUTH2_REDIRECT_URI,
            'scope': 'tweet.read users.read offline.access',
            'state': 'state',
            'code_challenge': 'challenge',
            'code_challenge_method': 'plain'
        }
        query_string = requests.compat.urlencode(params)
        twitter_auth_url = f'{authorization_url}?{query_string}'
        return redirect(twitter_auth_url)


class TwitterOauth2CallbackView(APIView):
    """Twitter로부터 리디렉션 받은 후 처리"""
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({'error': 'code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        token = TwitterClient().get_token(code=code)
        if not token:
            return Response({'error': 'token is required'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token.get('access_token')
        if not access_token:
            return Response({'error': 'access_token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = TwitterClient().get_user_info(access_token=access_token)
        if not user_info:
            return Response({'error': 'user_info is required'}, status=status.HTTP_400_BAD_REQUEST)
        username = user_info.get('data').get('username')
        return Response({'message': f'{username} twitter oauth 2.0 login success'}, status=status.HTTP_200_OK)
