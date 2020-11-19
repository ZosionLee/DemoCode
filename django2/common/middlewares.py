# * coding:utf-8 *
# Author: ZosionLee


import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.views import exception_handler

from common.exception import DjangoError, InternalError

logger = logging.getLogger('root')


class DummyMiddlewareOne(MiddlewareMixin):

    def process_request(self, request):
        print('Dummy middleware one, before handle request')
        return None

    def process_exception(self, request, exception):
        if isinstance(exception, (DjangoError, InternalError)):
            return JsonResponse(data=exception.body,
                                status=status.HTTP_400_BAD_REQUEST)
        response = exception_handler(exception, context=None)
        if response is not None:
            response.data['status_code'] = response.status_code
            return JsonResponse(data=response.data)
        else:
            body = InternalError(1100).body
            logger.error(body, exc_info=True)
            return JsonResponse(
                data=body, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def process_response(self, request, response):
        print('Dummy middleware one, after handle request')
        return response


class DummyMiddlewareTwo(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Dummy middleware two, before handle request')
        response = self.get_response(request)
        print('Dummy middleare two, after handle request')
        return response


def dummy_middleware_three(get_response):

    def middleware(request):
        print('Dummy middleware three, before handle request')
        response = get_response(request)
        print('Dummy middleare three, after handle request')
        return response

    return middleware
