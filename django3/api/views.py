# * coding:utf-8 *
# Author: ZosionLee

from asgiref.sync import sync_to_async
import asyncio

from django.http.response import JsonResponse
from django.utils.decorators import classonlymethod
from django.views.generic import View
from api.models import Students

class BaseView(View):

    def pagination(self,request,queryset):
        offset=request.GET.get('offset',None)
        limit=request.GET.get('limit',None)
        if not all((offset,limit)):
            return queryset
        try:
            offset,limit=int(offset),int(limit)
            if offset< 0 or limit < 0:
                raise Exception
        except Exception:
            raise ValueError('offset and limit must positive integer')
        return queryset[offset:offset+limit]


class StudentsView(BaseView):
    """Base Async View."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.async_queryset=sync_to_async(Students.queryset, thread_sensitive=True)

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    def to_dict(self,queryset):
        if queryset:
            return [
                {
                    'id':i.id,
                    'name':i.name,
                    'phone':i.phone,
                    'teacher':{
                        'id':i.teacher.id,
                        'name':i.teacher.name
                    },
                    'class':{
                        'id':i.cla.id,
                        'name':i.cla.name
                    }
                } for i in queryset
            ]
        return []

    async def get(self, request, *args, **kwargs):
        students=await  self.async_queryset()
        students=self.to_dict(self.pagination(request,students))
        return JsonResponse(students,safe=False)