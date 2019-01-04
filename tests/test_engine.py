# coding=utf-8
#
# Licensed under the MIT License
"""Dialog Engine test code."""
from chatql.engine import DialogEngine
from nose.tools import eq_, ok_
from collections import namedtuple


DummyScenario = namedtuple('DummyScenario', 'conditions response')
DummyUser = namedtuple('DummyUser', 'id')


class DummyDatabaseClient(object):
    def __init__(self):
        self._locals = {}
        self.scenarios = []

    def locals(self, user_id):
        return self._locals

    def create_new_user(self):
        return DummyUser(id="1")


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
        client._locals = {'a': 1}
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

    def test_generate_response_with_line_code(self):
        client = DummyDatabaseClient()
        conditions="""True \
            and True"""
        client.scenarios = [DummyScenario(conditions=conditions, response='OK!')]
        engine = DialogEngine(client)
        text = engine.generate_response_text('')
        eq_(text, 'OK!')

    def test_generate_response_with_white_space(self):
        client = DummyDatabaseClient()
        conditions="""
            True \
            and True
        """
        client.scenarios = [DummyScenario(conditions=conditions, response='OK!')]
        engine = DialogEngine(client)
        text = engine.generate_response_text('')
        eq_(text, 'OK!')

    def test_create_new_user(self):
        client = DummyDatabaseClient()
        engine = DialogEngine(client)
        eq_(engine.create_new_user(), "1")
