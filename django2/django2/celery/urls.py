# * coding:utf-8 *
# Author: ZosionLee



from django.contrib import admin
from django.urls import path
from task.view import CeleryDemo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/celery_demo', CeleryDemo.as_view()),
]
