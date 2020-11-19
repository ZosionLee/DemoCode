# * coding:utf-8 *
# Author: ZosionLee

import random
import logging

from django.db import transaction
from django.db.models import Q, Subquery, F, Count, Avg, Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from mimesis import Person
from common.models import *

logger=logging.getLogger('root')

class MockData(object):

    def __init__(self):
        self.p = Person()

    @property
    def teacher(self):
        return {
            'id': shortuuid.uuid(),
            'name': self.p.name()
        }

    @property
    def student(self):
        return {
            'id': shortuuid.uuid(),
            'name': self.p.name(),
            'phone': self.p.telephone()[:11]
        }

    @property
    def class_(self):
        return {
            'id': shortuuid.uuid(),
            'name': f'class-{random.randint(1,10)}'
        }

    @property
    def course(self):
        courses=['mathematics', 'physics', 'chemistry', 'biology', 'philosophy']
        return {
            'id': shortuuid.uuid(),
            'name': f'{random.choice(courses)}-{random.randint(1,10)}'
        }


class Insert(object):

    mock=MockData()

    @classmethod
    def bulk_insert(cls):
        '''example for class bulk create'''

        # step1: use mock to create models
        classes=[Classes(**cls.mock.class_) for _ in range(5)]
        teachers=[Teachers(**cls.mock.teacher) for _ in range(10)]
        courses=[Courses(**cls.mock.course) for _ in range(6)]

        students=[]
        for class_ in classes:
            teacher = random.choice(teachers)
            students.extend(
                Students(
                    teacher=teacher,
                    cla=class_,
                    **cls.mock.student
                ) for _ in range(30)
            )

        scores=[
            Scores(
                id=shortuuid.uuid(),
                student=student,
                course=course,
                score=random.randint(60, 100)
            ) for student in students for course in courses
        ]

        # step2: bulk insert in one transaction
        try:
            with transaction.atomic():
                Classes.objects.bulk_create(classes)
                Teachers.objects.bulk_create(teachers)
                Courses.objects.bulk_create(courses)
                Students.objects.bulk_create(students)
                Scores.objects.bulk_create(scores)
        except BaseException as e:
            logger.error(f'Insert error: {e}')
            raise

    @classmethod
    def joint_insert(cls):
        Classes.objects.create(
            id=shortuuid.uuid(),
            name='demo_class'
        )

    @classmethod
    def update_or_create(cls):
        id_=shortuuid.uuid()
        Teachers.objects.update_or_create(
            id=id_, defaults={'id':id_,'name':'teacher demo'}
        )



@receiver(pre_save, sender=Classes, dispatch_uid='joint_insert_student')
def joint_insert_teacher(sender, **kwargs):
    class_ = kwargs['instance']
    if class_.pk:
        teacher=Teachers.objects.first()
        Students.objects.create(
            id=shortuuid.uuid(),
            name='demo',
            phone='2369596',
            cla=class_,
            teacher=teacher
        )

class Update(object):

    @classmethod
    def bulk_update(cls):
        queryset=Scores.objects.\
            filter(courese__name='physics-1').all()
        for instance in queryset:
            if instance.score>90:
                instance.score=90
            elif 80 < instance.score < 90:
                instance.score=80
            elif 60 < instance.score < 80:
                instance.score=70
            else:
                instance.score=60
        Scores.objects.bulk_create(queryset,['score'])


class Query(object):

    @classmethod
    def get_count(cls):
        Students.objects.count()

    @classmethod
    def q_query(cls):
        queryset=Students.objects.\
            filter(Q(name__startswith='Dy') & Q(phone__endswith='8')).\
            only('id','name','phone').all()
        print(str(queryset.query))

        queryset = Students.objects. \
            filter(Q(name__startswith='Dy') | Q(phone__endswith='8')). \
            only('id', 'name', 'phone').all()
        print(str(queryset.query))

        queryset = Students.objects. \
            filter(~Q(phone__contains='-')). \
            only('id', 'name', 'phone').all()
        print(str(queryset.query))

        queryset = Students.objects.filter(name=F('name')). \
            only('id', 'name', 'phone').all()
        print(str(queryset.query))

    @classmethod
    def select_related(cls):
        queryset = Scores.objects.\
            select_related('student'). \
            select_related('student__teacher'). \
            select_related('student__cla'). \
            select_related('course').all()
        print(str(queryset.query))

    @classmethod
    def prefetch_related(cls):
        queryset=Students.objects.prefetch_related(
            Prefetch(
                'student',
                Scores.objects.select_related('course').all(),
                to_attr='scores'
            )).all()
        if queryset:
            print(str(queryset.query))

    @classmethod
    def combine_queryset(cls):
        students=Students.objects.only('id','name').all()[:10]
        teachers=Teachers.objects.only('id','name').all()[:10]
        conbine=students.union(teachers)
        print(conbine.query)

    @classmethod
    def subquery(cls):
        teachers=Teachers.objects.only('id').values('id')
        students=Students.objects.only('id','name').filter(teacher__in=Subquery(teachers))
        print(students.query)

        teachers = Teachers.objects.only('id').values('id')
        students = Students.objects.only('id', 'name').filter(teacher__in=teachers)
        print(students.query)

    @classmethod
    def annotate(cls):
        duplicated=Students.objects.values('name').\
            annotate(name_count=Count('name')).filter(name_count__gt=1)
        print(duplicated.query)

    @classmethod
    def aggregate(cls):
        avg=Scores.objects.aggregate(avg_score=Avg('score'))
        print(avg.query)


    @classmethod
    def student_avg_score(cls):
        avg=Scores.objects.select_related('student').\
            values('student__name').annotate(ascore=Avg('score')).\
            order_by('-ascore')
        print(avg.query)

    @classmethod
    def class_avg_score(cls):
        avg=Scores.objects.filter(course__name='biology-1').\
            select_related('student').\
            select_related('student__cla'). \
            values('student__cla__name').annotate(ascore=Avg('score'))
        print(avg.query)

        avg = Scores.objects.\
            select_related('student'). \
            select_related('student__cla'). \
            select_related('course').\
            values('student__cla__name','course__name').\
            annotate(ascore=Avg('score'))
        print(avg.query)

    @classmethod
    def outstanding_student(cls):
        outstanding=Scores.objects.select_related('student').\
            values('student__name').\
            filter(
            course__name__in=['chemistry-7','physics-1','biology-1']
        ).annotate(total=Sum('score')).order_by('-total')
        print(outstanding.query)


    @classmethod
    def student_count(cls):
        total = Students.objects.select_related('cla').\
            annotate(class_name=F('cla__name')). \
            values('class_name'). \
            annotate(total=Count('id'))
        print(total.query)



