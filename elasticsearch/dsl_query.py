# * coding:utf-8 *
# Author: ZosionLee


from pprint import pprint

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import (Fuzzy, Match, MatchAll, MoreLikeThis,
                                     MultiMatch, Q, Range)

from client import Client


class DslQuery(object):

    def __init__(self):
        self.client = Client().client

    def print_(self, t):
        if t.get('hits', {}).get('total', {}).get('value', None):
            hits = t['hits']['hits']
            for hit in hits:
                pprint(hit.get('_source'))

    def find_all(self):
        s = Search(using=self.client, index='book-index').execute()
        pprint(s.to_dict())

    def match_by_q(self):
        print('---' * 25 + 'multi match use Q' + '---' * 25)
        q = Q('multi_match', query='python', fields=['title', 'author'])
        s = Search(using=self.client, index='book-index')
        s = s.query(q).source(['title', 'author']).execute()
        self.print_(s.to_dict())

    def fuzzy_match_by_q(self):
        print('---' * 25 + 'fuzzy match use Q' + '---' * 25)
        q = Q(
            'multi_match',
            query='pjthen',
            fields=[
                'title',
                'author'],
            fuzziness='auto')
        s = Search(using=self.client, index='book-index')
        s = s.query(q).source(['title', 'author']).execute()
        self.print_(s.to_dict())

    def match_all(self):
        print('---' * 25 + 'MatchAll' + '---' * 25)
        s = Search(using=self.client, index='book-index')
        r = MatchAll()
        s = s.query(r).source(['title', 'publish_date']).execute()
        self.print_(s.to_dict())

    def match(self):

        print('---' * 25 + 'Match' + '---' * 25)
        m = Match(title={'query': 'python'})
        s = Search(using=self.client, index='book-index').query(m). \
            source(
            includes=['a*', 'title'],
            excludes=['p*']
        ).execute()
        self.print_(s.to_dict())

    def multi_math(self):
        print('---' * 25 + 'MultiMatch' + '---' * 25)
        m = MultiMatch(query='python', fields=['title', 'author'])
        s = Search(using=self.client, index='book-index').query(m). \
            source(['title', 'author']).execute()
        self.print_(s.to_dict())

    def range(self):
        print('---' * 25 + 'Range' + '---' * 25)
        s = Search(using=self.client, index='book-index')
        r = Range(publish_date={'gte': '2015-01-01', 'lte': '2020-12-31'})
        s = s.query(r).source(['title', 'publish_date', 'abstract']).execute()
        self.print_(s.to_dict())

    def more_like_this(self):
        print('---' * 25 + 'MoreLikeThis' + '---' * 25)
        s = Search(using=self.client, index='book-index')
        r = MoreLikeThis(like='where are my', fields=['abstract', ])
        s = s.query(r).source(['title', 'abstract']).execute()
        self.print_(s.to_dict())

    def bool_query(self):
        q = Q('match', title='python') | Q('match', title='java')
        q = q & Q('match', author='guido')
        q = ~Q('match', author='gosling') & q
        s = Search(using=self.client, index='book-index')
        s = s.query(q).source(['title', 'author']).execute()
        self.print_(s.to_dict())

    def filter_query(self):
        print('---' * 25 + 'range query' + '---' * 25)
        s = Search(using=self.client, index='book-index')
        s = s.filter(
            'range',
            publish_date={
                'gte': '2015-01-01',
                'lte': '2020-12-31'})
        s = s.source(['title', 'publish_date', 'comments', 'fans'])
        s = s.execute()
        self.print_(s.to_dict())

        print('---' * 25 + 'exact query' + '---' * 25)
        s = Search(using=self.client, index='book-index')
        s = s.filter('term', publication='wiley')
        s = s.source(['title', 'publication'])
        s = s.execute()
        self.print_(s.to_dict())

    def sort_and_pagination(self):
        print('---' * 25 + 'sort_and_pagination query' + '---' * 25)
        s = Search(using=self.client, index='book-index')
        s = s.filter(
            'range',
            publish_date={
                'gte': '2015-01-01',
                'lte': '2020-12-31'})
        s = s.source(['title', 'publish_date', 'comments', 'fans'])
        s = s.sort('comments', '-fans')
        s = s[3:6]
        s = s.execute()
        self.print_(s.to_dict())

    def field_value_factor(self):
        print('---' * 25 + 'FunctionScore: field_value_factor' + '---' * 25)
        q = Q(
            'function_score',
            query=Q(
                'multi_match',
                query='guido',
                fields=[
                    'title',
                    'author'],
                fuzziness='auto'),
            field_value_factor={
                'field': 'fans',
                'modifier': 'log1p',
                'factor': 3,
                'missing': 1}
        )
        s = Search(using=self.client, index='book-index')
        s = s.query(q).source(['title', 'fans', 'author']).execute()
        self.print_(s.to_dict())

    def painless_script_score(self):
        print('---' * 25 + 'FunctionScore: painless script score' + '---' * 25)
        q = Q(
            'function_score',
            query=Q('multi_match', query='python', fields=['title', 'author']),
            boost_mode='replace',
            script_score={
                'script': {
                    'lang': 'painless',
                    'params': {'x': 1, 'y': 2},
                    'source': '_score + params.y * doc["fans"].value + params.x'
                }
            }
        )
        s = Search(using=self.client, index='book-index')
        s = s.query(q).source(['title', 'fans', 'author']).execute()
        self.print_(s.to_dict())

    def random_score(self):
        print('---' * 25 + 'FunctionScore: random_score' + '---' * 25)
        q = Q(
            'function_score',
            query=Q('multi_match', query='python', fields=['title', 'author']),
            boost_mode='replace',
            random_score={'seed': 1, 'field': 'fans'}
        )
        s = Search(using=self.client, index='book-index')
        s = s.query(q).source(['title', 'fans', 'author']).execute()
        self.print_(s.to_dict())

    def function_score(self):
        print('---' * 25 + 'FunctionScore: function' + '---' * 25)
        q = Q(
            'function_score',
            query=Q('multi_match', query='python', fields=['title', 'author']),

            functions=[
                {
                    'filter': {'term': {'publication': 'harpercollins'}},
                    'weight': 10
                },
                {
                    'filter': {'term': {'publication': 'scholastic'}},
                    'weight': 20
                }
            ],
            boost=2,
            score_mode='max',
            boost_mode='replace',
            min_score=10
        )
        s = Search(using=self.client, index='book-index')
        s = s.query(q).source(['title', 'author', 'publication']).execute()
        self.print_(s.to_dict())

    def decay_function(self):
        print('---' * 25 + 'FunctionScore: decay function' + '---' * 25)
        q = Q(
            'function_score',
            query=Q('multi_match', query='python', fields=['title', 'author']),
            boost_mode='replace',
            functions=[
                {
                    'exp': {
                        'publish_date': {
                            'origin': '2018-09-15',
                            'offset': '15d',
                            'scale': '15d',
                            'decay': '0.3'
                        }
                    }
                }
            ]
        )
        s = Search(using=self.client, index='book-index')
        s = s.query(q).source(['title', 'author', 'publish_date']).execute()
        self.print_(s.to_dict())


if __name__ == '__main__':
    d = DslQuery()
    d.decay_function()
