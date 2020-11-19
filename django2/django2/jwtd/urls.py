# * coding:utf-8 *
# Author: ZosionLee



from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path(
        'v1/api/token',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'v1/api/token/refresh',
        TokenRefreshView.as_view(),
        name='token_refresh'),
    path(
        'v1/api/token/verify',
        TokenVerifyView.as_view(),
        name='token_verify'),
]
