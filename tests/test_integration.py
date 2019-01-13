# coding=utf-8
#
# Licensed under the MIT License
"""System Integration Test."""
import chatql
import subprocess
import json
import os
import time
import shutil
from nose.tools import eq_, ok_


dbpath = "mongodb"
process = None
client = None
engine = None


def setup():
    global process, client, engine
    if not os.path.exists(dbpath):
        os.mkdir(dbpath)
    process = subprocess.Popen("mongod --dbpath ./%s --port 27018" % dbpath, shell=True)
    client = chatql.mongodb_client.MongoClient(**{"db": "chatql", "port": 27018})
    engine = chatql.engine.DialogEngine(client)
    client.import_scenario("tests/test_scenario.json")


def teardown():
    process.terminate()
    time.sleep(1)
    shutil.rmtree(dbpath)


class TestIntegration:
    def teardown(self):
        chatql.mongodb_client.User.objects().delete()
        chatql.mongodb_client.History.objects().delete()

    def test_basic_access(self):
        query = '''
            query getResponse {
                response(request: "hello") {
                    id
                    text
                }
            }
        '''
        result = chatql.schema.execute(query, context={'engine': engine})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'Hello!')

    def test_basic_access_twice_no_user(self):
        query = '''
            query getResponse {
                response(request: "hello") {
                    id
                    text
                }
            }
        '''
        result = chatql.schema.execute(query, context={'engine': engine})
        result = chatql.schema.execute(query, context={'engine': engine})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'Hello!')

    def test_basic_access_twice_user(self):
        query = '''
            query getResponse($user: ID) {
                response(request: "hello", user: $user) {
                    id
                    text
                    user {
                        id
                    }
                }
            }
        '''
        result = chatql.schema.execute(query, context={'engine': engine})
        result = chatql.schema.execute(query, context={'engine': engine}, variables={'user': result.data['response']['user']['id']})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'Hello! Again!')

    def test_basic_access_matcher(self):
        query = '''
            query getResponse($user: ID) {
                response(request: "What's your name?", user: $user) {
                    id
                    text
                    user {
                        id
                    }
                }
            }
        '''
        result = chatql.schema.execute(query, context={'engine': engine})
        result = chatql.schema.execute(query, context={'engine': engine}, variables={'user': result.data['response']['user']['id']})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'My name is cahtql.')

    def test_basic_access_get_last(self):
        query = '''
            query getResponse($request: String!, $user: ID) {
                response(request: $request, user: $user) {
                    id
                    text
                    user {
                        id
                    }
                }
            }
        '''
        result = chatql.schema.execute(
            query, context={'engine': engine},
            variables={'request': 'Hello'})
        result = chatql.schema.execute(
            query, context={'engine': engine},
            variables={'request': 'nice to meet you', 'user': result.data['response']['user']['id']})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'Hello! Again!')

        result = chatql.schema.execute(
            query, context={'engine': engine},
            variables={'request': 'What\'s your name?', 'user': result.data['response']['user']['id']})
        result = chatql.schema.execute(
            query, context={'engine': engine},
            variables={'request': 'nice to meet you', 'user': result.data['response']['user']['id']})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'Nice to meet you too!')

        result = chatql.schema.execute(
            query, context={'engine': engine},
            variables={'request': 'nice to meet you', 'user': result.data['response']['user']['id']})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'Hello! Again!')

    def test_basic_access_create_user(self):
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
        result = chatql.schema.execute(query, context={'engine': engine}, variables={"optionalArgs": json.dumps({"aaa": "aaa"})})
        eq_(result.errors, None)
        ok_(result.data['createUser']['user']['id'] is not None)
        eq_(result.data['createUser']['user']['optionalArgs'], '{"aaa": "aaa"}')

        query = '''
            query getUser($id: ID!) {
                user(id: $id) {
                    id
                    optionalArgs
                }
            }
        '''
        user_id = result.data['createUser']['user']['id']
        result = chatql.schema.execute(query, context={'engine': engine}, variables={"id": user_id})
        eq_(result.errors, None)
        eq_(result.data['user']['id'], user_id)
        eq_(result.data['user']['optionalArgs'], '{"aaa": "aaa"}')

    def test_basic_access_get_user_with_attributes(self):
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
        result = chatql.schema.execute(query, context={'engine': engine}, variables={"optionalArgs": json.dumps({"aaa": "aaa"})})
        eq_(result.errors, None)
        ok_(result.data['createUser']['user']['id'] is not None)
        eq_(result.data['createUser']['user']['optionalArgs'], '{"aaa": "aaa"}')

        query = '''
            query getUser($optionalArgs: String) {
                user(optionalArgs: $optionalArgs) {
                    id
                    optionalArgs
                }
            }
        '''
        user_id = result.data['createUser']['user']['id']
        result = chatql.schema.execute(query, context={'engine': engine}, variables={"optionalArgs": json.dumps({"aaa": "aaa"})})
        eq_(result.errors, None)
        eq_(result.data['user']['id'], user_id)
        eq_(result.data['user']['optionalArgs'], '{"aaa": "aaa"}')

    def test_basic_access_get_user_is_none(self):
        query = '''
            query getUser($optionalArgs: String) {
                user(optionalArgs: $optionalArgs) {
                    id
                    optionalArgs
                }
            }
        '''
        result = chatql.schema.execute(query, context={'engine': engine}, variables={"optionalArgs": json.dumps({"aaa": "aaa"})})
        eq_(result.errors, None)
        eq_(result.data['user']['id'], None)
