# coding=utf-8
#
# Licensed under the MIT License
"""GraphQL accessor test code."""
import json
import chatql
from graphql import GraphQLError
from chatql import __version__
from nose.tools import eq_, ok_
from collections import namedtuple


DummyUser = namedtuple('DummyUser', 'id')
DummyHistory = namedtuple('DummyHistory', 'id user scenario')


def test_version():
    assert __version__ == '0.1.0'


class DummyEngine:
    def generate_response_text(self, request, **kwargs):
        user = kwargs.get("user", None)
        if request == 'hello':
            return DummyHistory(id='111', user=DummyUser(id=user), scenario={"response": "hello!"})
        else:
            if user == '333':
                return DummyHistory(id='111', user=DummyUser(id=user), scenario={"response": "OK!"})
            else:
                return DummyHistory(id='111', user=DummyUser(id=user), scenario={"response": "what\'s?"})

    def create_new_user(self, **option):
        return "111"

    def get_user_attributes(self, user_id):
        return {"aaa": "aaa"}


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
        result = chatql.schema.execute(query, context={"engine": DummyEngine()})
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
        result = chatql.schema.execute(query, context={"engine": DummyEngine()})
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
        result = chatql.schema.execute(query, context={"engine": DummyEngine()}, variables={'request': 'hello'})
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
        result = chatql.schema.execute(query, context={"engine": DummyEngine()})
        eq_(result.errors, None)
        eq_(result.data['createUser']['user']['id'], "111")

    def test_create_user_add_option(self):
        query = '''
            mutation createUser($optionalArgs: String) {
                createUser(optionalArgs: $optionalArgs) {
                    user {
                        id
                        optionalArgs
                    }
                }
            }
        '''
        result = chatql.schema.execute(query, context={"engine": DummyEngine()}, variables={"optionalArgs": json.dumps({"aaa": "aaa"})})
        eq_(result.errors, None)
        eq_(result.data['createUser']['user']['id'], "111")
        eq_(result.data['createUser']['user']['optionalArgs'], "{\"aaa\": \"aaa\"}")

    def test_get_user_attributes(self):
        query = '''
            query getUser($id: ID!) {
                user(id: $id) {
                    id
                }
            }
        '''
        result = chatql.schema.execute(query, context={"engine": DummyEngine()}, variables={'id': '222'})
        eq_(result.errors, None)
        eq_(result.data['user']['id'], "222")

    def test_get_user_attributes_with_option(self):
        query = '''
            query getUser($id: ID!) {
                user(id: $id) {
                    id
                    optionalArgs
                }
            }
        '''
        result = chatql.schema.execute(query, context={'engine': DummyEngine()}, variables={"id": "222"})
        eq_(result.errors, None)
        eq_(result.data['user']['id'], "222")
        eq_(result.data['user']['optionalArgs'], '{"aaa": "aaa"}')

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
        result = chatql.schema.execute(query, context={"engine": DummyEngine()}, variables={'request': 'hello', 'user': '222'})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'hello!')
        eq_(result.data['response']['user']['id'], '222')

    def test_response_hello_with_specific_user(self):
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
        result = chatql.schema.execute(query, context={"engine": DummyEngine()}, variables={'request': 'OK!', 'user': '333'})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'OK!')
        eq_(result.data['response']['user']['id'], '333')
