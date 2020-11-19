# * coding:utf-8 *
# Author: ZosionLee



import functools
import traceback
from typing import List, Optional
import graphene
from django.core.handlers.wsgi import WSGIRequest
from graphene_django.views import GraphQLView
from graphql.error import GraphQLLocatedError, GraphQLSyntaxError,format_error
from rest_framework.exceptions import AuthenticationFailed

from common.customization import CustomAuthentication
from common.exception import DjangoError, InternalError


class CustomType(graphene.Scalar):
    @staticmethod
    def serialize(dt):
        return dt


class QueryUtils(object):

    @staticmethod
    def query_filter(
            queryset,
            query_params: Optional[List[dict]] = None
    ):
        if query_params:
            kwargs = {}
            for item in query_params:
                if item.get('field_value', None):
                    if item.get('lookup_expr', None):
                        key = item['field_name'] + '__' + item['lookup_expr']
                        kwargs[key] = item['field_value']
                    else:
                        kwargs[item['field_name']] = item['field_value']
            return queryset.filter(**kwargs)
        return queryset


    @staticmethod
    def order(queryset, field):
        if field:
            return queryset.order_by(field)
        return queryset


def authenticate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = getattr(args[1], 'context', None)
        if isinstance(request, WSGIRequest):
            CustomAuthentication().authenticate(request)
        else:
            raise AuthenticationFailed('HTTP 401: Unauthorized')
        return func(*args, **kwargs)
    return wrapper


class GraphQLAPIView(GraphQLView):

    def execute_graphql_request(self, *args, **kwargs):
        result = super().execute_graphql_request(*args, **kwargs)
        if result.invalid:
            '''you can logger error here'''
            pass
        return result

    @staticmethod
    def format_located_error(error):
        if isinstance(error.original_error, GraphQLLocatedError):
            return GraphQLAPIView.format_located_error(error.original_error)
        if isinstance(error.original_error, (DjangoError, InternalError)):
            return error.original_error.body
        else:
            return {
                'exception': type(error.original_error).__name__,
                'message': str(error.original_error),
                'trace': traceback.format_list(traceback.extract_tb(error.__traceback__)),
            }

    @staticmethod
    def format_error(error):
        try:
            if isinstance(error, GraphQLLocatedError):
                return GraphQLAPIView.format_located_error(error)
            if isinstance(error, GraphQLSyntaxError):
                return format_error(error)
        except Exception as e:
            return  {
                'exception': type(error).__name__,
                'message': str(error),
                'trace': traceback.format_list(traceback.extract_tb(error.__traceback__)),
            }

