# coding=utf-8
#
# Licensed under the MIT License
"""GraphQL accessor test code."""
import chatql
from chatql import __version__
from nose.tools import eq_


def test_version():
    assert __version__ == '0.1.0'


class TestQL:
    def test_query_hello(self):
        query = '''
            query getResponse {
                response {
                    id
                    text
                }
            }
        '''
        result = chatql.schema.execute(query)
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'hello!')
