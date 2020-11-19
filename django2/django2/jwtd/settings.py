# * coding:utf-8 *
# Author: ZosionLee



from datetime import timedelta

from django2.settings import *

SITE_ID = 1

ROOT_URLCONF = 'django2.jwtd.urls'
INSTALLED_APPS += [
    'jwtd',
]

WSGI_APPLICATION = 'django2.jwtd.wsgi.application'
AUTHENTICATION_BACKENDS = ['jwtd.authentication.CustomAuthBackend', ]
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}
