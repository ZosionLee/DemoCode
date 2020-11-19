# * coding:utf-8 *
# Author: ZosionLee


from rest_framework.filters import OrderingFilter
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from common.customization import (CustomAuthentication, CustomPagination,
                                  CustomPermission)
from common.exception import DjangoError
from common.models import Teachers
from common.serializers import TeachersSerializer


class TeachersView(ListCreateAPIView):

    authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomPermission, ]
    filter_backends = (OrderingFilter,)
    pagination_class = CustomPagination
    serializer_class = TeachersSerializer
    queryset = Teachers.objects.all()
    ordering = ('-created_at',)


class TeacherView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomPermission, ]
    serializer_class = TeachersSerializer

    def get_object(self):
        id = self.kwargs.get('id', None)
        instance = Teachers.objects.filter(id=id).first()
        if self.request.method == 'PUT':
            if not instance:
                raise DjangoError(1005)
            return instance
        else:
            return instance
