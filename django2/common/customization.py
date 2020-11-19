# * coding:utf-8 *
# Author: ZosionLee


from collections import OrderedDict

from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from common.models import Students
from common.utils import JwtUtils


class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """Authenticate"""
        authorization_heaader = request.headers.get('Authorization', None)
        if not authorization_heaader:
            raise AuthenticationFailed('HTTP 401: Unauthorized')
        access_token = authorization_heaader.split(' ')[1]
        JwtUtils.verify_token(access_token)
        return 'success', True

    def authenticate_header(self, request):
        return 'token'


class CustomPagination(LimitOffsetPagination):
    '''
    pagination
    '''
    limit_query_param = 'count'
    default_limit = 999999

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('all', self.count),
            ('items', data)
        ]), status=status.HTTP_200_OK)


class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        print('dummy permission')
        return True


class StudentFilter(filters.FilterSet):

    name = filters.CharFilter(
        field_name='name', lookup_expr='contains'
    )
    phone = filters.CharFilter(
        field_name='phone', lookup_expr='contains'
    )

    class Meta:
        model = Students
        fields = ['name', 'phone']
