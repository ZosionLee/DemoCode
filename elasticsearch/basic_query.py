# * coding:utf-8 *
# Author: ZosionLee


from pprint import pprint

from client import Client


class BasicQuery(object):

    def __init__(self):
        self.client = Client().client

    def print_(self, t):
        if t.get('hits', {}).get('total', {}).get('value', None):
            hits = t['hits']['hits']
            for hit in hits:
                pprint(hit.get('_source'))

    def count(self):
        count = self.client.count(index='book-index')
        pprint(f'Count:{count}')

    def all(self):
        t = self.client.search(index='book-index', )  # 10 sources
        self.print_(t)

    def match(self):
        print('---' * 25 + 'match' + '---' * 25)
        dsl = {
            'query': {
                'match': {
                    'title': 'python'
                }
            }
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def multi_match(self):
        # multi match and boosting author score
        print('---' * 25 + 'multi_match' + '---' * 25)
        dsl = {
            'query': {
                'multi_match': {
                    'query': 'George',
                    'fields': ['title', 'author^3']
                }
            }
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def bool_query(self):
        # bool query: must --AND, must_not -- NOT, should -- OR
        dsl = {
            'query': {
                'bool': {
                    'must': {
                        'bool': {
                            'should': [
                                {'match': {'title': 'Python'}},
                                {'match': {'title': 'Java'}},
                                {'match': {'title': 'Golang'}}
                            ],
                            'must': {'match': {'author': 'Guido'}}
                        }
                    },
                    'must_not': {'match': {'author': 'Gosling'}}
                }
            }
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def fuzzy_query(self):

        # Fuzzy Queries
        print('---' * 25 + 'Fuzzy Queries' + '---' * 25)
        dsl = {
            'query': {
                'multi_match': {
                    'query': 'Guide vans Rossom',  # word speel error
                    'fields': ['title', 'author'],
                    'fuzziness': 'AUTO'
                }
            },
            '_source': ['title', 'author'],
            'size': 1
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def wildcard_query(self):
        print('---' * 25 + 'Wildcard Query' + '---' * 25)
        dsl = {
            'query': {
                'wildcard': {
                    'author': '*haka'
                }
            },
            '_source': ['title', 'author'],
            'highlight': {
                'fields': {
                    'author': {}
                }
            }
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def regex_query(self):
        print('---' * 25 + 'Regexp Query' + '---' * 25)
        dsl = {
            'query': {
                'wildcard': {
                    'title': 'p[a-z]*n'
                }
            },
            '_source': ['title', 'author'],
            'highlight': {
                'fields': {
                    'author': {}
                }
            }
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def match_phrase(self):
        '''
        match phase and match phase prefix,
        slop: move words
        max_expansions: number of words matched by the prefix
        :return:
        '''
        print('---' * 25 + 'match_phrase' + '---' * 25)
        dsl = {
            'query': {
                'match_phrase': {
                    'abstract': {
                        'query': 'Erlang is known systems',
                        'slop': 10,
                    }
                }
            },
            '_source': ['title', 'abstract']
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def match_phrase_prefix(self):
        print('---' * 25 + 'match_phrase_prefix' + '---' * 25)
        dsl = {
            'query': {
                'match_phrase_prefix': {
                    'abstract': {
                        'query': 'Erlang is kn',
                        'slop': 10,
                        'max_expansions': 10,
                    }
                }
            },
            '_source': ['title', 'abstract']
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def exact_query(self):
        '''
        terms and term
        :return:
        '''
        dsl = {
            'query': {
                'term': {
                    'publication': 'harpercollins'  # not support space
                }
            },
            '_source': ['title', 'publication']
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def range_query(self):
        '''range and sorted query'''
        dsl = {
            'query': {
                'range': {
                    'publish_date': {
                        'gte': '2015-01-01',
                        'lte': '2020-12-31'
                    }
                }
            },
            '_source': ['title', 'publish_date', 'comments', 'fans'],
            'sort': [
                {'comments': {'order': 'desc'}},
                {'fans': {'order': 'asc'}}
            ]
        }

        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)

    def filter_query(self):
        '''deleted after 5.5'''
        pass

    def function_score(self):
        dsl = {
            'query': {
                'function_score': {
                    'query': {
                        'multi_match': {
                            'query': 'gosling',
                            'fields': ['title', 'author']
                        }
                    },
                    'field_value_factor': {
                        'field': 'fans',
                        'modifier': 'log2p',
                        'factor': 2
                    }
                }
            },
            '_source': ['title', 'fans', 'author']
        }
        t = self.client.search(index='book-index', body=dsl)
        self.print_(t)


if __name__ == '__main__':
    b = BasicQuery()
    b.count()
    b.bool_query()
