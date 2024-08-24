from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.clients.google import GoogleClient
from accounts.constants import GOOGLE_ACCOUNT_URL


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
