# * coding:utf-8 *
# Author: ZosionLee

import functools
import json
import logging
from threading import RLock
from typing import Optional
from urllib import parse

import arrow
import requests
from cerberus import Validator
from rest_framework.exceptions import AuthenticationFailed

from common.exception import DjangoError, InternalError

logger = logging.getLogger('root')


class Singleton(type):
    _instances = {}
    _lock = RLock()

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instances:
            with Singleton._lock:
                if cls not in Singleton._instances:
                    Singleton._instances[cls] = super().__call__(
                        *args, **kwargs)
        return Singleton._instances[cls]


class TimeUtils(object):

    @classmethod
    def datetime_format(cls, dt):
        return arrow.get(dt).format()


class JwtUtils(object):

    host = 'http://127.0.0.1:8001'

    @classmethod
    def get_token(cls, username, password):
        url = parse.urljoin(cls.host, 'v1/api/token')
        logger.info(f'Request({url}) for token')
        try:
            res = requests.post(
                url=url,
                data={'username': username, 'password': password},

            )
        except Exception as e:
            logger.error(f'Request for jwt token error: {e}')
            raise e
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 401:
            raise DjangoError(1002)
        else:
            logger.error(f'Request for jwt token error: {res.reason}')
            raise AssertionError('Bad request')

    @classmethod
    def verify_token(cls, token):
        url = parse.urljoin(cls.host, 'v1/api/token/verify')
        logger.info(f'Request({url}) for token verify')
        try:
            res = requests.post(
                url=url,
                data={'token': token},
            )
        except Exception as e:
            logger.error(f'Request for jwt token verify error: {e}')
            raise e
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 401:
            logger.error(f'Request for jwt token error: {res.reason}')
            raise AuthenticationFailed('HTTP 401: Unauthorized')
        else:
            logger.error(f'Request for jwt token error: {res.reason}')
            raise AssertionError('Bad request')


class SchemaValidation(object):

    @classmethod
    def validate(cls,data,schema):
        v = Validator()
        try:
            res=v.validate(data,schema)
        except Exception as e:
            logger.error(f'Schema error:{e}')
            raise InternalError(1100)
        if not res:
            logger.error(f'Schema error:{v.errors}')

    @classmethod
    def schema_validate(
            cls,
            body_schema: Optional[dict] = None,
            query_schema: Optional[dict] = None
    ):
        def wrapper(method):
            @functools.wraps(method)
            def inner(request, *args, **kwargs):
                if query_schema:
                    SchemaValidation.validate(request.query_params, query_schema)
                if body_schema:
                    content_type = request.content_type \
                        if request.content_type else 'application/json'
                    if content_type != 'application/json':
                        raise DjangoError(1003)
                    else:
                        try:
                            json_body = json.loads(request.body)
                        except BaseException:
                            raise DjangoError(1003)
                        SchemaValidation.validate(json_body, body_schema)
                return method(request, *args, **kwargs)

            return inner

        return wrapper


