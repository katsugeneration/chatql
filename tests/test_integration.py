# coding=utf-8
#
# Licensed under the MIT License
"""System Integration Test."""
import chatql
import subprocess
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
            query getResponse {
                response(request: "hello", user: "111111111111111111111111") {
                    id
                    text
                }
            }
        '''
        result = chatql.schema.execute(query, context={'engine': engine})
        result = chatql.schema.execute(query, context={'engine': engine})
        eq_(result.errors, None)
        eq_(result.data['response']['text'], 'Hello! Again!')
