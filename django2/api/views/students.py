# * coding:utf-8 *
# Author: ZosionLee

from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from common.customization import (CustomAuthentication, CustomPagination,
                                  CustomPermission, StudentFilter)
from common.exception import DjangoError
from common.models import Students
from common.schema import Definition
from common.serializers import StudentsSerializer
from common.utils import SchemaValidation


@method_decorator(
    SchemaValidation.schema_validate(
        body_schema=Definition['add_student']),name='post')
class StudentsView(ListCreateAPIView):

    # authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomPermission, ]
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    pagination_class = CustomPagination
    serializer_class = StudentsSerializer
    filter_class = StudentFilter
    queryset = Students.queryset()
    ordering = ('-created_at',)


class StudentView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomPermission, ]
    serializer_class = StudentsSerializer

    def get_object(self):
        id_ = self.kwargs.get('id', None)
        instance = Students.get_object(id_)
        if self.request.method == 'PUT':
            if not instance:
                raise DjangoError(1005)
            return instance
        else:
            return instance
