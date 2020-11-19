# * coding:utf-8 *
# Author: ZosionLee



from django.contrib.auth.backends import ModelBackend

from common.models import Users


class CustomAuthBackend(ModelBackend):

    def authenticate(self,
                     request,
                     username=None,
                     password=None,
                     **kwargs):
        if not username or not password:
            return None
        user = Users.objects.filter(name=username).first()
        if user:
            if user.password == password:
                return user
        return None

    def get_user(self, user_id):
        user = Users.objects.filter(id=user_id).first()
        if not user:
            return None
        return user
