# * coding:utf-8 *
# Author: ZosionLee


from client import Client
from elasticsearch import helpers
from mock import Book, Person


class InsertData(object):

    def __init__(self):
        self.client = Client().client
        self.person = Person()
        self.book = Book()

    def insert_person(self, persons=None):
        if not self.client.indices.exists('person'):
            self.client.indices.create(index='person')
        if not persons:
            persons = self.person.create_person(10)
        for person in persons:
            self.client.create(
                index='person',
                doc_type='social_person',
                id=person.get('id'),
                body=person
            )

    def insert_books(self):
        books = Book(50)()
        actions = [
            {
                '_index': 'book-index',
                '_id': book.get('id'),
                '_source': book
            } for book in books
        ]
        helpers.bulk(self.client, actions)


if __name__ == '__main__':
    i = InsertData()
    i.insert_person()
    i.insert_books()
