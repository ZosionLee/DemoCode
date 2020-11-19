# * coding:utf-8 *
# Author: ZosionLee


from rest_framework.filters import OrderingFilter
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from common.customization import (CustomAuthentication, CustomPagination,
                                  CustomPermission)
from common.exception import DjangoError
from common.models import Courses
from common.serializers import CoursesSerializer


class CoursesView(ListCreateAPIView):

    authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomPermission, ]
    filter_backends = (OrderingFilter,)
    pagination_class = CustomPagination
    serializer_class = CoursesSerializer
    queryset = Courses.objects.all()
    ordering = ('-created_at',)


class CourseView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomPermission, ]
    serializer_class = CoursesSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        instance = Courses.objects.filter(id=id).first()
        if self.request.method == 'PUT':
            if not instance:
                raise DjangoError(1005)
            return instance
        else:
            return instance
