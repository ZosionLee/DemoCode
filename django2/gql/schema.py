# * coding:utf-8 *
# Author: ZosionLee


import graphene

from common.utils import JwtUtils
from gql.common import authenticate
from gql.models import *


class Query(graphene.ObjectType):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    teacher= graphene.Field(TeacherType, id=graphene.String())
    teachers=graphene.Field(
        TeachersType,
        offset=graphene.String(),
        limit=graphene.String()
    )
    class_ = graphene.Field(ClassType, id=graphene.String())
    classes = graphene.Field(
        ClassesType,
        offset=graphene.String(),
        limit=graphene.String()
    )

    course = graphene.Field(CourseType, id=graphene.String())
    courses = graphene.Field(
        CoursesType,
        offset=graphene.String(),
        limit=graphene.String()
    )

    student = graphene.Field(StudentType, id=graphene.String())
    students = graphene.Field(
        StudentsType,
        name=graphene.String(),
        phone=graphene.String(),
        offset=graphene.String(),
        limit=graphene.String()
    )

    score = graphene.Field(ScoreType, id=graphene.String())
    scores = graphene.Field(
        ScoresType,
        offset=graphene.String(),
        limit=graphene.String()
    )

    @authenticate
    def resolve_teacher(self, info, **kwargs):
        id_=kwargs.get('id','')
        return Teachers.objects.filter(id=id_).first()

    @authenticate
    def resolve_teachers(self, info, **kwargs):
        offset, limit = (
            kwargs.get('offset', None),
            kwargs.get('limit', None)
        )
        queryset = TeachersType.order(Teachers.objects.all(), '-created_at')
        queryset.coffset, queryset.climit = offset, limit
        return queryset

    @authenticate
    def resolve_class_(self, info, **kwargs):
        id_ = kwargs.get('id', '')
        return Classes.objects.filter(id=id_).first()

    @authenticate
    def resolve_classes(self, info, **kwargs):
        offset, limit = (
            kwargs.get('offset', None),
            kwargs.get('limit', None)
        )
        queryset = ClassesType.order(Classes.objects.all(), '-created_at')
        queryset.coffset, queryset.climit = offset, limit
        return queryset

    @authenticate
    def resolve_course(self, info, **kwargs):
        id_ = kwargs.get('id', '')
        return Courses.objects.filter(id=id_).first()

    @authenticate
    def resolve_courses(self, info, **kwargs):
        offset, limit = (
            kwargs.get('offset', None),
            kwargs.get('limit', None)
        )
        queryset = CoursesType.order(Courses.objects.all(), '-created_at')
        queryset.coffset, queryset.climit = offset, limit
        return queryset

    @authenticate
    def resolve_student(self,info,**kwargs):
        id_ = kwargs.get('id', '')
        return Students.objects.filter(id=id_).first()

    @authenticate
    def resolve_students(self,info,**kwargs):
        name,phone,offset, limit = (
            kwargs.get('name', None),
            kwargs.get('phone', None),
            kwargs.get('offset', None),
            kwargs.get('limit', None)
        )
        query_params = [
            {
                'field_name': 'name',
                'field_value': name,
                'lookup_expr': 'contains'
            },
            {
                'field_name': 'phone',
                'field_value': phone,
                'lookup_expr': 'contains'
            },
        ]
        queryset=Students.objects.select_related('teacher').select_related('cla').all()
        queryset= TeachersType.query_filter(queryset,query_params)
        queryset = TeachersType.order(queryset, '-created_at')
        queryset.coffset,queryset.climit=offset,limit
        return queryset

    @authenticate
    def resolve_score(self, info, **kwargs):
        id_ = kwargs.get('id', '')
        return Scores.objects.filter(id=id_).first()

    @authenticate
    def resolve_scores(self, info, **kwargs):
        offset, limit = (
            kwargs.get('offset', None),
            kwargs.get('limit', None)
        )
        queryset = Students.objects.\
            select_related('student').\
            select_related('student__teacher'). \
            select_related('student__cla'). \
            select_related('course').all()
        queryset = TeachersType.order(queryset, '-created_at')
        queryset.coffset, queryset.climit = offset, limit
        return queryset

class UserLogin(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        res = JwtUtils.get_token(username, password)
        user=Users.objects.filter(name=username,password=password).first()
        user.access_token=res.get('access','')
        user.refresh_token=res.get('refresh','')
        return UserLogin(user=user)

class Mutation(graphene.ObjectType):
    user_login = UserLogin.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    auto_camelcase=False
)