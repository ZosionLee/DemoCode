# * coding:utf-8 *
# Author: ZosionLee


'''
python manage.py inspectdb > models.py
use ForeignKey to establish relationship
'''
from django.db import models
from django.db.models import Prefetch


class Classes(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        managed = False
        db_table = 'classes'


class Courses(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        managed = False
        db_table = 'courses'


class Scores(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    student = models.ForeignKey(
        to='Students',
        on_delete=models.DO_NOTHING,
        db_column='stu_id',
        db_constraint=False,
        max_length=22,
        null=True,
        related_name='student'
    )
    course = models.ForeignKey(
        to='Courses',
        on_delete=models.DO_NOTHING,
        db_column='cou_id',
        db_constraint=False,
        max_length=22,
        null=True,
        related_name='course'
    )
    score = models.IntegerField()

    @classmethod
    def get_object(cls, id_):
        return cls.objects.filter(id=id_).\
            select_related('student').\
            select_related('student__teacher').\
            select_related('student__cla').\
            select_related('course').first()

    @classmethod
    def queryset(cls):
        queryset = cls.objects.\
            select_related('student'). \
            select_related('student__teacher'). \
            select_related('student__cla'). \
            select_related('course').all()
        return queryset

    class Meta:
        managed = False
        db_table = 'stu_courses'


class Students(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=11)
    teacher = models.ForeignKey(
        to='Teachers',
        on_delete=models.DO_NOTHING,
        db_column='teacher_id',
        db_constraint=False,
        max_length=22,
        null=True,
        related_name='teacher'
    )
    cla = models.ForeignKey(
        to='Classes',
        on_delete=models.DO_NOTHING,
        db_column='class_id',
        db_constraint=False,
        max_length=22,
        null=True,
        related_name='cla'
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    @classmethod
    def get_object(cls, id_):
        return cls.objects.filter(id=id_). \
            prefetch_related(
            Prefetch(
                'student',
                Scores.objects.select_related('course').all(),
                to_attr='scores'
            )
        ).select_related('teacher').select_related('cla').first()

    @classmethod
    def queryset(cls):
        return cls.objects.prefetch_related(
            Prefetch(
                'student',
                Scores.objects.select_related('course').all(),
                to_attr='scores'
            )). \
            select_related('teacher'). \
            select_related('cla').all()

    class Meta:
        managed = False
        db_table = 'students'


class Teachers(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        managed = False
        db_table = 'teachers'


class Users(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    @property
    def is_active(self):
        return True

    class Meta:
        managed = False
        db_table = 'users'
