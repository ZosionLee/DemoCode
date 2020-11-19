# * coding:utf-8 *
# Author: ZosionLee


import uuid
from pprint import pprint

from client import Client


class IndexTemplate(object):

    def __init__(self):
        self.client = Client().client

    @property
    def settings(self):
        return {
            'analysis': {
                'analyzer': {
                    'custom_analyzer': {
                        'type': 'custom',
                        'char_filter': ['split-word', '&&-to-and'],
                        'tokenizer': 'punctuation',
                        'filter': ['lowercase', 'kill-stopword', 'kill-currency']
                    }
                },
                'char_filter': {
                    '&&-to-and': {
                        'type': 'mapping',
                        'mappings': ['&&=> and ']
                    },
                    'split-word': {
                        'type': 'pattern_replace',
                        'pattern': '(?<=\\p{Lower})(?=\\p{Upper})',
                        'replacement': ' '
                    },
                },
                'tokenizer': {
                    'punctuation': {
                        'type': 'pattern',
                        'pattern': '[ .,!?]'
                    }
                },
                'filter': {
                    'kill-stopword': {
                        'type': 'stop',
                        'ignore_case': True,
                        'stopwords': ['is', 'at', 'but', 'or', 'and']
                    },
                    'kill-currency': {
                        'type': 'pattern_replace',
                        'pattern': '[$|€|￡|￥]',
                        'replacement': '',
                        'all': False
                    }
                }
            },
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    @property
    def mappings(self):
        return {
            'properties': {
                'first_name': {
                    'type': 'text',
                    'copy_to': 'author_name',
                    'doc_values': False
                },
                'last_name': {
                    'type': 'text',
                    'copy_to': 'author_name',
                    'doc_values': False
                },
                'author_name': {
                    'type': 'text',
                    'fields': {
                        'raw': {
                            'type': 'keyword'
                        }
                    },
                },
                'author_age': {
                    'type': 'integer',
                    'coerce': True
                },
                'title': {
                    'type': 'text',
                    'boost': 2
                },
                'abstract': {
                    'type': 'text',
                    'fielddata': True,
                    'fielddata_frequency_filter': {
                        'min': 0.01,
                        'max': 0.2,
                        'min_segment_size': 100
                    }
                },
                'score': {
                    'type': 'integer_range',
                },
                'created_at': {
                    'type': 'date',
                },
                'published_date': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd'
                },
                'sales': {
                    'type': 'nested',
                    'dynamic': False,
                    'properties': {
                        'Amazon': {'type': 'integer'},
                        'eBay': {'type': 'integer'},
                        'PayPay ': {'type': 'integer'},
                        'Taobao ': {'type': 'integer'}
                    }
                }
            }
        }

    def create_template(self):
        t = {
            'aliases': {
                'demo-data': {}
            },
            'settings': self.settings,
            'mappings': self.mappings,
            'order': 0,
            'template': 'demo*'
        }
        if self.client.indices.exists_template('demo_one'):
            self.client.indices.delete_template('demo_one')
            if self.client.indices.exists('demo_index_one'):
                self.client.indices.delete('demo_index_one')
        self.client.indices.put_template(name='demo_one', body=t, create=True)
        self.client.create(
            index='demo_index_one',
            body={
                'first_name': 'James',
                'last_name': 'Bond',
                'title': 'This is a demo book'
            },
            id=uuid.uuid1().hex
        )

    def show_info(self):
        mappings = self.client.indices.get_mapping('demo_index_one')
        settings = self.client.indices.get_settings('demo_index_one')
        print('-' * 30 + 'demo_index_one mappings' + '-' * 30)
        pprint(mappings)
        print('-' * 30 + 'demo_index_one settings' + '-' * 30)
        pprint(settings)

    def remove_template(self):
        if self.client.indices.exists_template('demo_one'):
            self.client.indices.delete_template('demo_one')


if __name__ == '__main__':
    t = IndexTemplate()
    t.create_template()
    t.show_info()
    t.remove_template()
