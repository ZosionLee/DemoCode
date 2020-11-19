# * coding:utf-8 *
# Author: ZosionLee


import logging
from collections import Mapping, OrderedDict

import shortuuid
from django.db import transaction
from django.db.models import Q
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, DateTimeField, set_value
from rest_framework.settings import api_settings

from common.exception import DjangoError, InternalError
from common.models import Classes, Courses, Scores, Students, Teachers, Users
from common.utils import TimeUtils

logger = logging.getLogger('root')


class MyDateTimeField(DateTimeField):
    def to_representation(self, value):
        return TimeUtils.datetime_format(value)


class BaseSerializer(serializers.ModelSerializer):
    id = CharField()
    created_at = MyDateTimeField()

    def _short_uuid_check(self, id_):
        try:
            if len(id_) != 22:
                raise ValueError
            shortuuid.ShortUUID(id_)
        except ValueError:
            raise DjangoError(1004)

    def to_internal_value(self, data):
        '''
        shut fields validation down
        '''
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        fields = self._writable_fields
        for field in fields:
            primitive_value = field.get_value(data)
            set_value(ret, field.source_attrs, primitive_value)
        return ret


class CTCBaseSerializer(BaseSerializer):
    '''Base for class, teacher and course'''

    def _name_duplicated(self):
        name = self.initial_data.get('name', None)
        if self.instance:
            if self.Meta.model.objects.filter(name=name). \
                    exclude(name=self.instance.name).exists():
                raise DjangoError(1006)
        else:
            if self.Meta.model.objects.filter(name=name).exists():
                raise DjangoError(1006)

    def validate(self, data):
        self._name_duplicated()
        return self.initial_data

    def create(self, validated_data):
        kwargs = {
            'id': shortuuid.uuid(),
            'name': validated_data.get('name', '')
        }
        try:
            with transaction.atomic():
                self.instance = self.Meta.model.objects.create(**kwargs)
        except BaseException as e:
            logger.error(f'Create class entity error:{e}')
        return self.instance

    def update(self, instance, validated_data):
        _id = self.instance.id
        name = validated_data.get('name', '')
        try:
            with transaction.atomic():
                self.Meta.model.objects.select_for_update(). \
                    filter(id=_id).update(name=name)
        except BaseException as e:
            logger.error(f'Update class entity error:{e}')
            raise InternalError(1102)
        instance = self.Meta.model.objects.get(id=_id)
        return instance

    class Meta:
        model = None
        fields = ('id', 'name', 'created_at')


class ClassesSerializer(CTCBaseSerializer):
    '''serializer for classes'''

    class Meta:
        model = Classes
        fields = ('id', 'name', 'created_at')


class TeachersSerializer(CTCBaseSerializer):
    '''serializer for teachers'''

    class Meta:
        model = Classes
        fields = ('id', 'name', 'created_at')


class CoursesSerializer(CTCBaseSerializer):
    '''serializer for teachers'''

    class Meta:
        model = Courses
        fields = ('id', 'name', 'created_at')


class StudentsSerializer(BaseSerializer):
    '''serializer for students'''

    teacher = serializers.SerializerMethodField()
    class_ = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()

    @staticmethod
    def get_teacher(instance):
        return TeachersSerializer(instance.teacher).data

    @staticmethod
    def get_class_(instance):
        return ClassesSerializer(instance.cla).data

    @staticmethod
    def get_scores(instance):
        if hasattr(instance, 'scores'):
            return [
                {
                    'course': model_to_dict(i.course),
                    'score': i.score
                } for i in instance.scores
            ]
        return []

    def _name_phone_duplicated(self):
        name = self.initial_data.get('name', None)
        phone = self.initial_data.get('phone', None)
        if self.instance:
            if Students.objects.filter(Q(name=name) | Q(phone=phone)). \
                    exclude(Q(name=self.instance.name) | Q(phone=self.instance.phone)).\
                    exists():
                raise DjangoError(1006)
        else:
            if Students.objects.filter(Q(name=name) | Q(phone=phone)).exists():
                raise DjangoError(1006)

    def _class_exist(self):
        class_id = self.initial_data.get('class_id', '')
        self._short_uuid_check(class_id)
        if not Classes.objects.filter(id=class_id).exists():
            raise DjangoError(1008)

    def _teacher_exist(self):
        teacher_id = self.initial_data.get('teacher_id', '')
        self._short_uuid_check(teacher_id)
        if not Teachers.objects.filter(id=teacher_id).exists():
            raise DjangoError(1007)

    def validate(self, data):
        self._name_phone_duplicated()
        self._class_exist()
        self._teacher_exist()
        return self.initial_data

    def create(self, validated_data):
        kwargs = {
            'id': shortuuid.uuid(),
            'name': self.validated_data['name'],
            'phone': self.validated_data['phone'],
            'teacher_id': self.validated_data['teacher_id'],
            'cla_id': self.validated_data['class_id']
        }
        try:
            with transaction.atomic():
                self.instance = Students.objects.create(**kwargs)
        except BaseException as e:
            logger.error(f'Create student entity error:{e}')
        return self.instance

    def update(self, instance, validated_data):
        _id = self.instance.id
        kwargs = {
            'name': self.validated_data['name'],
            'phone': self.validated_data['phone'],
            'teacher_id': self.validated_data['teacher_id'],
            'cla_id': self.validated_data['class_id']
        }
        try:
            with transaction.atomic():
                Students.objects.select_for_update(). \
                    filter(id=_id).update(**kwargs)
        except BaseException as e:
            logger.error(f'Update student entity error:{e}')
            raise InternalError(1102)
        instance = Students.get_object(_id)
        return instance

    class Meta:
        model = Students
        fields = ('id','name','phone','created_at','teacher','class_','scores')


class ScoresSerializer(BaseSerializer):
    '''serializer for score'''

    student = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()

    @staticmethod
    def get_student(instance):
        return StudentsSerializer(instance.student).data

    @staticmethod
    def get_course(instance):
        return CoursesSerializer(instance.course).data

    def _score_duplicated(self):
        student_id = self.initial_data.get('student_id', None)
        course_id = self.initial_data.get('course_id', None)
        if Scores.objects.filter(
                student__id=student_id, course__id=course_id
        ).exists():
            raise DjangoError(1006)

    def _student_exist(self):
        student_id = self.initial_data.get('student_id', '')
        self._short_uuid_check(student_id)
        if not Students.objects.filter(id=student_id).exists():
            raise DjangoError(1009)

    def _course_exist(self):
        course_id = self.initial_data.get('course_id', '')
        self._short_uuid_check(course_id)
        if not Courses.objects.filter(id=course_id).exists():
            raise DjangoError(1010)

    def validate(self, data):
        if not self.instance:
            self._score_duplicated()
            self._student_exist()
            self._course_exist()
        return self.initial_data

    def create(self, validated_data):
        kwargs = {
            'id': shortuuid.uuid(),
            'student_id': self.validated_data['student_id'],
            'course_id': self.validated_data['course_id'],
            'score': self.validated_data['score'],
        }
        try:
            with transaction.atomic():
                self.instance = Scores.objects.create(**kwargs)
        except BaseException as e:
            logger.error(f'Create score entity error:{e}')
        return self.instance

    def update(self, instance, validated_data):
        _id = self.instance.id
        kwargs = {
            'score': self.validated_data['score'],
        }
        try:
            with transaction.atomic():
                Scores.objects.select_for_update(). \
                    filter(id=_id).update(**kwargs)
        except BaseException as e:
            logger.error(f'Update score entity error:{e}')
            raise InternalError(1102)
        instance = Scores.get_object(_id)
        return instance

    class Meta:
        model = Scores
        fields = ('id', 'score', 'student', 'course')


class UsersSerializer(BaseSerializer):

    class Meta:
        model = Users
        fields = ('id', 'name')
