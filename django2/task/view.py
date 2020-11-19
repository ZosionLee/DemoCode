# * coding:utf-8 *
# Author: ZosionLee

import random
import time

import shortuuid
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from task.tasks import eat_fruit, eat_vegetable, report


class CeleryDemo(ListCreateAPIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fruits=[
            'banana', 'apple', 'pear', 'prunes', 'strawberry',
            'raspberry', 'blueberry', 'pomegranate', 'durian',
            'mangosteen', 'watermelon', 'cantaloupe', 'plum',
            'lychee', 'longan', 'mango'
        ]
        self.vegetable=[
            'leek','broccoli','chives','lettuce',
            'cauliflower','daikon','carrot','tomato',
            'potato','pumpkin' ,'asparagus' ,'mushroom'
        ]


    def list(self, request, *args, **kwargs):

        for _ in range(10):
            eat_fruit.delay(random.choice(self.fruits))
        eat_vegetable.delay(random.choice(self.vegetable))
        for i in range(20):
            report.delay(
                id=shortuuid.uuid(), msg=f'This is report {i}'
            )
        return Response('Success')

    def create(self, request, *args, **kwargs):
        while True:
            eat_fruit.delay(random.choice(self.fruits))
            eat_vegetable.delay(random.choice(self.vegetable))
            time.sleep(1)



