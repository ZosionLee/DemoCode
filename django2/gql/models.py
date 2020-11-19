# * coding:utf-8 *
# Author: ZosionLee

import graphene

from common.models import *

from graphene_django import DjangoObjectType

from gql.common import QueryUtils


class UserType(DjangoObjectType):

    access_token = graphene.String()
    refresh_token = graphene.String()

    def resolve_access_token(self, info):
        if hasattr(self,'access_token'):
            return self.access_token
        return ''

    def resolve_refresh_token(self, info):
        if hasattr(self,'refresh_token'):
            return self.refresh_token
        return ''

    class Meta:
        model = Users
        fields = ('id','name')


class ListType(graphene.ObjectType,QueryUtils):
    total = graphene.Int()

    @classmethod
    def slice(cls,queryset, offset, limit):
        if offset and limit:
            try:
                offset, limit = int(offset), int(limit)
                if offset < 0 or limit < 0:
                    return ValueError()
            except (ValueError, TypeError) as e:
                raise e
            return queryset[offset:offset + limit]
        return queryset

    def resolve_total(self, info):
        return self.count()

    def resolve_items(self, info):
        if hasattr(self,'climit') and hasattr(self,'coffset'):
            return ListType.slice(self,self.coffset,self.climit)
        return self

    class Meta:
        fields = ('total', 'items')

class ClassType(DjangoObjectType):
    class Meta:
        model = Classes
        fields = ('id','name','created_at')

class ClassesType(ListType):
    items = graphene.List(ClassType)

class TeacherType(DjangoObjectType):
    class Meta:
        model = Teachers
        fields = ('id','name','created_at')

class TeachersType(ListType):
    items = graphene.List(TeacherType)

class CourseType(DjangoObjectType):
    class Meta:
        model = Courses
        fields = ('id','name','created_at')

class CoursesType(ListType):
    items = graphene.List(CourseType)

class StudentType(DjangoObjectType):
    class Meta:
        model = Students
        fields = ('id','name','phone','teacher','cla','created_at')

class StudentsType(ListType):
    items = graphene.List(StudentType)

class ScoreType(DjangoObjectType):
    class Meta:
        model = Scores
        fields = ('id','course','student','score')

class ScoresType(ListType):
    items = graphene.List(ScoreType)

