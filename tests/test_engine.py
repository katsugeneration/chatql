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

    @property
    def scenarios(self):
        return [
            DummyScenario(conditions='True', response='OK!')
        ]


class TestEngine:
    def test_generate_response(self):
        engine = DialogEngine(DummyDatabaseClient())
        text = engine.generate_response_text('')
        eq_(text, 'OK!')
