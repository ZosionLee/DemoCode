# * coding:utf-8 *
# Author: ZosionLee


from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from common.customization import (CustomAuthentication, CustomPagination,
                                  CustomPermission)
from common.exception import DjangoError
from common.models import Scores
from common.serializers import ScoresSerializer


class ScoresView(ListCreateAPIView):

    # authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomPermission, ]
    pagination_class = CustomPagination
    serializer_class = ScoresSerializer
    queryset = Scores.queryset()


class ScoreView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [CustomAuthentication, ]
    permission_classes = [CustomPermission, ]
    serializer_class = ScoresSerializer

    def get_object(self):
        id_ = self.kwargs.get('id', None)
        instance = Scores.get_object(id_)
        if self.request.method == 'PUT':
            if not instance:
                raise DjangoError(1005)
            return instance
        else:
            return instance
