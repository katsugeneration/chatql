# coding=utf-8
#
# Licensed under the MIT License
"""Mongodb client test code."""
from chatql.mongodb_client import MongoClient, Scenario, User, History
import datetime
import mongoengine
from nose.tools import eq_, ok_, raises


class TestClient:
    def setup(self):
        self.client = MongoClient()

    def test_add_scenario(self):
        Scenario.objects().delete()
        s = Scenario()
        s.save()
        eq_(s.id, Scenario.objects().only('id').first().id)

    def test_add_scenario_check_created_at(self):
        Scenario.objects().delete()
        s = Scenario()
        s.save()
        utc = datetime.datetime.utcnow()
        ok_(utc >= s.created_at >= utc - datetime.timedelta(seconds=1))
        ok_(utc >= s.modified_at >= utc - datetime.timedelta(seconds=1))

    def test_add_scenario_update_modified(self):
        Scenario.objects().delete()
        s = Scenario()
        s.save()
        utc = datetime.datetime.utcnow()
        __import__("time").sleep(1)
        s.response = 'aaa'
        s.save()
        utc_modified = datetime.datetime.utcnow()
        eq_(s.response, 'aaa')
        ok_(utc >= s.created_at >= utc - datetime.timedelta(seconds=1))
        ok_(utc_modified >= s.modified_at >= utc_modified - datetime.timedelta(seconds=1))

    def test_add_scenario_attributes(self):
        Scenario.objects().delete()
        s = Scenario(attributes={'id': '111'})
        s.save()
        eq_(s.id, Scenario.objects(attributes__id='111').only('id').first().id)

    def test_add_scenario_check_client_property(self):
        Scenario.objects().delete()
        eq_(len(self.client.scenarios), 0)
        s = Scenario()
        s.save()
        eq_(len(self.client.scenarios), 1)

    def test_add_user(self):
        User.objects().delete()
        u = User()
        u.save()
        eq_(u.id, User.objects().only('id').first().id)

    def test_add_user_add_any_attributes(self):
        User.objects().delete()
        u = User()
        u.favotire = 'sports'
        u.save()
        eq_(u.id, User.objects(favotire='sports').only('id').first().id)

    def test_add_history(self):
        History.objects().delete()
        User.objects().delete()
        u = User()
        h = History()
        h.user_id = u
        h.scenario = {"response": "aaa"}
        u.save()
        h.save()
        eq_(h.id, History.objects().only('id').first().id)

    def test_add_history_check_created_at(self):
        History.objects().delete()
        User.objects().delete()
        u = User()
        h = History()
        h.user_id = u
        h.scenario = {"response": "aaa"}
        u.save()
        h.save()
        utc = datetime.datetime.utcnow()
        ok_(utc >= h.created_at >= utc - datetime.timedelta(seconds=1))

    @raises(mongoengine.errors.ValidationError)
    def test_add_history_no_user(self):
        History.objects().delete()
        User.objects().delete()
        h = History()
        h.scenario = {"response": "aaa"}
        h.save()

    @raises(mongoengine.errors.ValidationError)
    def test_add_history_no_scenario(self):
        History.objects().delete()
        User.objects().delete()
        u = User()
        h = History()
        h.user_id = u
        u.save()
        h.save()

    def test_client_locals(self):
        eq_(History, self.client.locals["history"])
