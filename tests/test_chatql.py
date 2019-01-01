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

    def get_new_user_id(self):
        return "111"


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

    def test_create_user(self):
        query = '''
            mutation createUser {
                createUser {
                    user {
                        id
                    }
                }
            }
        '''
        result = chatql.schema.execute(query, context={"data_accessor": DummyDataAccessor()})
        eq_(result.errors, None)
        eq_(result.data['createUser']['user']['id'], "111")

    def test_get_user(self):
        query = '''
            query getUser($id: ID!) {
                user(id: $id) {
                    id
                }
            }
        '''
        result = chatql.schema.execute(query, context={"data_accessor": DummyDataAccessor()}, variables={'id': '222'})
        eq_(result.errors, None)
        eq_(result.data['user']['id'], "222")

    def test_response_hello_with_user(self):
        query = '''
            query getResponse($request: String!, $user: ID) {
                response(request: $request, user: $user) {
                    id
                    user {
                        id
                    }
                    text
                }
            }
        '''
        result = chatql.schema.execute(query, context={"data_accessor": DummyDataAccessor()}, variables={'request': 'hello', 'user': '222'})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'hello!')
        eq_(result.data['response']['user']['id'], '222')
