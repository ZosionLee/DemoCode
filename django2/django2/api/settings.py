# * coding:utf-8 *
# Author: ZosionLee


from django2.settings import *

SITE_ID = 1

ROOT_URLCONF = 'django2.api.urls'
INSTALLED_APPS += [
    'api',
]

MIDDLEWARE = MIDDLEWARE + [
    'common.middlewares.DummyMiddlewareOne',
    'common.middlewares.DummyMiddlewareTwo',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

WSGI_APPLICATION = 'django2.api.wsgi.application'
