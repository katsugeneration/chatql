# coding=utf-8
#
# Licensed under the MIT License
"""Dialog Engine test code."""
from chatql.engine import DialogEngine
from nose.tools import eq_, ok_
from collections import namedtuple


DummyScenario = namedtuple('DummyScenario', 'conditions response attributes')
DummyUser = namedtuple('DummyUser', 'id')
DummyHistory = namedtuple('DummyHistory', 'id user scenario request')


class DummyDatabaseClient(object):
    def __init__(self):
        self._globals = {}
        self.scenarios = []
        self._history = []

    def globals(self, user):
        return self._globals

    def create_new_user(self, **option):
        return DummyUser(id="1")

    def get_user_attributes(self, user_id):
        return {"aaa": "aaa"}

    def save_history(self, request, scenario, user):
        self._history.append((request, scenario, user))
        return DummyHistory(id='', request=request, scenario=scenario, user=user)


class TestEngine:
    def test_generate_response(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='True', response='OK!', attributes={})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_check_save_history(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='True', response='OK!', attributes={})]
        engine = DialogEngine(client)
        engine.generate_response_text('', user='111')
        eq_(client._history[0][0], '')
        eq_(client._history[0][1], client.scenarios[0])
        eq_(client._history[0][2], '111')

    def test_generate_response_check_save_history_response_None(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='False', response='OK!', attributes={})]
        engine = DialogEngine(client)
        engine.generate_response_text('', user='111')
        eq_(client._history[0][0], '')
        eq_(client._history[0][1], None)
        eq_(client._history[0][2], '111')

    def test_generate_response_with_user_is_none(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions="True", response='OK!', attributes={})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')
        eq_(client._history[0][2], '1')

    def test_generate_response_wuthout_condition_is_true(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='False', response='OK!', attributes={})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        ok_(resposne.scenario is None)

    def test_generate_response_with_globals(self):
        client = DummyDatabaseClient()
        client._globals = {'a': 1}
        client.scenarios = [DummyScenario(conditions='a == 1', response='OK!', attributes={})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_request(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='regex("a*?")', response='OK!', attributes={})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('aaa')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_other_value(self):
        client = DummyDatabaseClient()
        client.scenarios = [DummyScenario(conditions='aaa == "bbb"', response='OK!', attributes={})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('', aaa='bbb')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_line_code(self):
        client = DummyDatabaseClient()
        conditions="""True \
            and True"""
        client.scenarios = [DummyScenario(conditions=conditions, response='OK!', attributes={})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_white_space(self):
        client = DummyDatabaseClient()
        conditions="""
            True \
            and True
        """
        client.scenarios = [DummyScenario(conditions=conditions, response='OK!', attributes={})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_generate_response_with_attributes(self):
        client = DummyDatabaseClient()
        conditions = """attributes['id'] == '111'"""
        client.scenarios = [DummyScenario(conditions=conditions, response='OK!', attributes={"id": "111"})]
        engine = DialogEngine(client)
        resposne = engine.generate_response_text('')
        eq_(resposne.scenario.response, 'OK!')

    def test_create_new_user(self):
        client = DummyDatabaseClient()
        engine = DialogEngine(client)
        eq_(engine.create_new_user(), "1")

    def test_create_new_user_with_option(self):
        client = DummyDatabaseClient()
        engine = DialogEngine(client)
        eq_(engine.create_new_user(option={"aaa": "aaa"}), "1")

    def test_get_user_attributes(self):
        client = DummyDatabaseClient()
        engine = DialogEngine(client)
        eq_(engine.get_user_attributes("111"), {"aaa": "aaa"})
