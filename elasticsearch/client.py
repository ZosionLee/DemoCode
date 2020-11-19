# * coding:utf-8 *
# Author: ZosionLee


from elasticsearch import Elasticsearch


class Client(object):

    def __init__(self):
        self.es = Elasticsearch(
            hosts=[
                'http://127.0.0.1:9200',
                'http://127.0.0.1:9201',
                'http://127.0.0.1:9202',
            ]
        )

    @property
    def client(self):
        return self.es
