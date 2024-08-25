from django.urls import path
from accounts.views import (
    GoogleLoginView, GoogleCallbackView, KakaoLoginView, KaKaoCallbackView, TwitterLoginView, TwitterCallbackView,
    TwitterOauth2LoginView, TwitterOauth2CallbackView
)

urlpatterns = [
    path('google/login', GoogleLoginView.as_view(), name='google-login'),
    path('google/callback', GoogleCallbackView.as_view(), name='google-callback'),
    path('kakao/login', KakaoLoginView.as_view(), name='kakao-login'),
    path('kakao/callback', KaKaoCallbackView.as_view(), name='kakao-callback'),
    path('twitter/login', TwitterLoginView.as_view(), name='twitter-login'),
    path('twitter/callback', TwitterCallbackView.as_view(), name='twitter-callback'),
    path('twitter/v2/login', TwitterOauth2LoginView.as_view(), name='twitter-login-v2'),
    path('twitter/v2/callback', TwitterOauth2CallbackView.as_view(), name='twitter-callback-v2'),
]
