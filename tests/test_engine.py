# coding=utf-8
#
# Licensed under the MIT License
"""Dialog Engine test code."""
from chatql.engine import DialogEngine
from nose.tools import eq_, ok_
from collections import namedtuple


DummyScenario = namedtuple('DummyScenario', 'conditions response')


class DummyDatabaseClient(object):
    def __init__(self):
        self.locals = {}
        self.scenarios = []


class TestEngine:
    def test_generate_response(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='True', response='OK!')]
        engine = DialogEngine(client)
        text = engine.generate_response_text('')
        eq_(text, 'OK!')

    def test_generate_response_wuthout_condition_is_true(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='False', response='OK!')]
        engine = DialogEngine(client)
        text = engine.generate_response_text('')
        ok_(text is None)

    def test_generate_response_with_locals(self):
        client = DummyDatabaseClient()
        client.locals = {'a': 1}
        client.scenarios = [DummyScenario(conditions='a == 1', response='OK!')]
        engine = DialogEngine(client)
        text = engine.generate_response_text('')
        eq_(text, 'OK!')

    def test_generate_response_with_request(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='request == "aaa"', response='OK!')]
        engine = DialogEngine(client)
        text = engine.generate_response_text('aaa')
        eq_(text, 'OK!')

    def test_generate_response_with_other_value(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='aaa == "bbb"', response='OK!')]
        engine = DialogEngine(client)
        text = engine.generate_response_text('', aaa='bbb')
        eq_(text, 'OK!')
