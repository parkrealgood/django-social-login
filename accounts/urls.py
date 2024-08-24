from django.urls import path
from accounts.views import GoogleLoginView, GoogleCallbackView

urlpatterns = [
    path('google/login', GoogleLoginView.as_view(), name='google-login'),
    path('google/callback', GoogleCallbackView.as_view(), name='google-callback'),
]
