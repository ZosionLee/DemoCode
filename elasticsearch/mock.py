# * coding:utf-8 *
# Author: ZosionLee


import random
import uuid

from mimesis import Datetime, Text
from mimesis.schema import Field, Schema


class Person(object):

    def create_person(self, num):
        _ = Field('en')
        description = (
            lambda: {
                'id': _('uuid'),
                'name': _('person.name'),
                'gender': _('person.gender'),
                'info': {
                    'first_name': _('person.first_name'),
                    'last_name': _('person.last_name'),
                    'height': _('person.height'),
                    'weight': _('person.weight'),
                    'email': _('person.email'),
                    'telephone': _('person.telephone'),
                    'nationality': _('person.nationality'),
                    'academic_degree': _('person.academic_degree'),
                    'blood_type': _('person.blood_type'),
                    'social_media_profile': _('person.social_media_profile'),
                    'occupation': _('person.occupation'),
                    'address': {
                        'country': _('address.country'),
                        'region': _('address.region'),
                        'state': _('address.state'),
                        'city': _('address.city'),
                        'street_number': _('address.street_number'),
                        'street_name': _('address.street_name'),
                        'postal_code': _('address.postal_code'),
                        'geo_info': {
                            'longitude': _('address.longitude'),
                            'latitude': _('address.latitude')
                        }
                    }
                }
            }
        )
        schema = Schema(schema=description)
        return schema.create(iterations=num)


class Book(object):

    def __init__(self, num=None):
        self.num = num if num else 1

    @property
    def title(self):
        t = [
            'Python - Guido van Rossum', 'Java - James Gosling', 'Thinking in python',
            'Data Structure for python', 'Handoop cook book',
            'Golang cookbook', 'C# cookbook', 'C programing - Dennis Ritchie'
        ]
        return random.choice(t)

    @property
    def author(self):
        t = [
            'Dennis Ritchie', 'Ken Thompson', 'Guido van Rossum',
            'James Gosling', 'Anders Hejlsberg', ' Larry Wall',
            'George Ross Ihaka', 'Robert C. Pike', 'Brendan Eich',
            'Brad Cox', 'Rasmus Lerdorf', 'Bjarne Stroustrup',
            'Alan Cooper'
        ]
        num = random.choice([1, 2, 3])
        authors = [random.choice(t) for _ in range(0, num)]
        return authors

    @property
    def abstract(self):
        t = Text()
        return t.sentence()

    @property
    def publish_date(self):
        t = Datetime()
        return t.datetime()

    @property
    def publication(self):
        p = [
            'Penguin Random House', 'Hachette Livre', 'HarperCollins',
            'Macmillan Publishers', 'Simon & Schuster', 'Scholastic',
            'Springer', 'Wiley', 'Shueisha'
        ]
        return random.choice(p)

    def __call__(self, *args, **kwargs):
        return [
            {
                'id': uuid.uuid1().hex,
                'author': self.author,
                'title': self.title,
                'abstract': self.abstract,
                'publish_date': self.publish_date,
                'publication': self.publication,
                'comments': random.randint(1, 1000),
                'fans': random.randint(1, 1000)
            } for _ in range(0, self.num)
        ]
