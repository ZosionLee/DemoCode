# * coding:utf-8 *
# Author: ZosionLee


from django2.settings import *

SITE_ID = 1


ROOT_URLCONF = 'django2.celery.urls'
INSTALLED_APPS += [
    'task',
]

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_ACCEPT_CONTENT = ['json',]
CELERY_BROKER_URL = f'redis://127.0.0.1:6379/1'


WSGI_APPLICATION = 'django2.celery.wsgi.application'

