from django.urls import path
from accounts.views import (
    GoogleLoginView, GoogleCallbackView, KakaoLoginView, KaKaoCallbackView, TwitterLoginView, TwitterCallbackView
)

urlpatterns = [
    path('google/login', GoogleLoginView.as_view(), name='google-login'),
    path('google/callback', GoogleCallbackView.as_view(), name='google-callback'),
    path('kakao/login', KakaoLoginView.as_view(), name='kakao-login'),
    path('kakao/callback', KaKaoCallbackView.as_view(), name='kakao-callback'),
    path('twitter/login', TwitterLoginView.as_view(), name='twitter-login'),
    path('twitter/callback', TwitterCallbackView.as_view(), name='twitter-callback'),
]
