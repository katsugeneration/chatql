# coding=utf-8
#
# Licensed under the MIT License
"""Dialog Engine test code."""
from chatql.engine import DialogEngine
from nose.tools import eq_, ok_
from collections import namedtuple


DummyScenario = namedtuple('DummyScenario', 'conditions response')
DummyUser = namedtuple('DummyUser', 'id')
DummyHistory = namedtuple('DummyHistory', 'id user_id scenario request')


class DummyDatabaseClient(object):
    def __init__(self):
        self._locals = {}
        self.scenarios = []
        self._history = []

    def locals(self, user_id):
        return self._locals

    def create_new_user(self):
        return DummyUser(id="1")

    def save_history(self, request, scenario, user_id):
        self._history.append((request, scenario, user_id))
        return DummyHistory(id='', request=request, scenario=scenario, user_id=user_id)


class TestEngine:
    def test_generate_response(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='True', response='OK!')]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_check_save_history(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='True', response='OK!')]
        engine = DialogEngine(client)
        engine.generate_response_text('', user_id='111')
        eq_(client._history[0][0], '')
        eq_(client._history[0][1], client.scenarios[0])
        eq_(client._history[0][2], '111')

    def test_generate_response_check_save_history_response_None(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='False', response='OK!')]
        engine = DialogEngine(client)
        engine.generate_response_text('', user_id='111')
        eq_(client._history[0][0], '')
        eq_(client._history[0][1], None)
        eq_(client._history[0][2], '111')

    def test_generate_response_with_user_is_none(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions="True", response='OK!')]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')
        eq_(client._history[0][2], '1')

    def test_generate_response_wuthout_condition_is_true(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='False', response='OK!')]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        ok_(resposne.scenario is None)

    def test_generate_response_with_locals(self):
        client = DummyDatabaseClient()
        client._locals = {'a': 1}
        client.scenarios = [DummyScenario(conditions='a == 1', response='OK!')]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_request(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='request == "aaa"', response='OK!')]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('aaa')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_other_value(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='aaa == "bbb"', response='OK!')]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('', aaa='bbb')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_line_code(self):
        client = DummyDatabaseClient()
        conditions="""True \
            and True"""
        client.scenarios = [DummyScenario(conditions=conditions, response='OK!')]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_white_space(self):
        client = DummyDatabaseClient()
        conditions="""
            True \
            and True
        """
        client.scenarios = [DummyScenario(conditions=conditions, response='OK!')]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_create_new_user(self):
        client = DummyDatabaseClient()
        engine = DialogEngine(client)
        eq_(engine.create_new_user(), "1")
