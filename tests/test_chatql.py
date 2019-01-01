# coding=utf-8
#
# Licensed under the MIT License
"""GraphQL accessor test code."""
import chatql
from graphql import GraphQLError
from chatql import __version__
from nose.tools import eq_, ok_


def test_version():
    assert __version__ == '0.1.0'


class DummyDataAccessor:
    def get_response_text(self, request):
        if request == 'hello':
            return 'hello!'
        else:
            return 'what\'s?'


class TestQL:
    def test_response_hello(self):
        query = '''
            query getResponse {
                response(request: "hello") {
                    id
                    text
                }
            }
        '''
        result = chatql.schema.execute(query, context={"data_accessor": DummyDataAccessor()})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'hello!')

    def test_response_no_hello(self):
        query = '''
            query getResponse {
                response(request: "OK!") {
                    id
                    text
                }
            }
        '''
        result = chatql.schema.execute(query, context={"data_accessor": DummyDataAccessor()})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'what\'s?')

    def test_response_hello_with_variables(self):
        query = '''
            query getResponse($request: String!) {
                response(request: $request) {
                    id
                    text
                }
            }
        '''
        result = chatql.schema.execute(query, context={"data_accessor": DummyDataAccessor()}, variables={'request': 'hello'})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'hello!')

    def test_response_hello_without_argument(self):
        query = '''
            query getResponse {
                response {
                    id
                    text
                }
            }
        '''
        result = chatql.schema.execute(query)
        ok_(isinstance(result.errors[0], GraphQLError))
