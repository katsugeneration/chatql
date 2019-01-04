# coding=utf-8
#
# Licensed under the MIT License
"""Mongodb client test code."""
from chatql.mongodb_client import MongoClient, Scenario, User, History
import datetime
import mongoengine
import os
import shutil
import time
import subprocess
from nose.tools import eq_, ok_, raises


dbpath = "mongodb"
process = None


def setup():
    global process
    if not os.path.exists(dbpath):
        os.mkdir(dbpath)
    process = subprocess.Popen("mongod --dbpath ./%s --port 27018" % dbpath, shell=True)


def teardown():
    process.terminate()
    time.sleep(1)
    shutil.rmtree(dbpath)


class TestClient:
    def setup(self):
        self.client = MongoClient(**{"db": "chatql", "port": 27018})

    def teardown(self):
        Scenario.objects().delete()
        User.objects().delete()
        History.objects().delete()

    def test_add_scenario(self):
        s = Scenario()
        s.save()
        eq_(s.id, Scenario.objects().only('id').first().id)

    def test_add_scenario_check_created_at(self):
        s = Scenario()
        s.save()
        utc = datetime.datetime.utcnow()
        ok_(utc >= s.created_at >= utc - datetime.timedelta(seconds=1))
        ok_(utc >= s.modified_at >= utc - datetime.timedelta(seconds=1))

    def test_add_scenario_update_modified(self):
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
        s = Scenario(attributes={'id': '111'})
        s.save()
        eq_(s.id, Scenario.objects(attributes__id='111').only('id').first().id)

    def test_add_scenario_check_client_property(self):
        eq_(len(self.client.scenarios), 0)
        s = Scenario()
        s.save()
        eq_(len(self.client.scenarios), 1)

    def test_add_user(self):
        u = User()
        u.save()
        eq_(u.id, User.objects().only('id').first().id)

    def test_add_user_add_any_attributes(self):
        u = User()
        u.favotire = 'sports'
        u.save()
        eq_(u.id, User.objects(favotire='sports').only('id').first().id)

    def test_add_history(self):
        u = User()
        h = History()
        h.user = u
        h.scenario = {"response": "aaa"}
        u.save()
        h.save()
        eq_(h.id, History.objects().only('id').first().id)

    def test_add_history_check_created_at(self):
        u = User()
        h = History()
        h.user = u
        h.scenario = {"response": "aaa"}
        u.save()
        h.save()
        utc = datetime.datetime.utcnow()
        ok_(utc >= h.created_at >= utc - datetime.timedelta(seconds=1))

    def test_add_history_no_user(self):
        h = History()
        h.scenario = {"response": "aaa"}
        h.save()

    def test_add_history_no_scenario(self):
        u = User()
        h = History()
        h.user = u
        u.save()
        h.save()

    def test_client_locals_history(self):
        u = User()
        h = History()
        h.user = u
        h.scenario = {"response": "aaa"}
        u.save()
        h.save()
        eq_(u.id, self.client.locals(u.id)["history"].only('user').first().user.id)

    def test_client_locals_history_with_user(self):
        u = User()
        h = History()
        h.user = u
        h.scenario = {"response": "aaa"}
        u.save()
        h.save()
        u = User()
        h = History()
        h.user = u
        h.scenario = {"response": "aaa"}
        u.save()
        h.save()
        eq_(len(History.objects()), 2)
        eq_(len(self.client.locals(u.id)["history"]), 1)

    def test_client_locals_user_with_user(self):
        u = User()
        u.save()
        eq_(u.id, self.client.locals(u.id)["user"].only('id').first().id)

    def test_client_locals_user(self):
        u = User()
        u.save()
        u = User()
        u.save()
        eq_(len(User.objects()), 2)
        eq_(len(self.client.locals(u.id)["user"]), 1)

    def test_create_new_user(self):
        u = self.client.create_new_user()
        eq_(u.id, User.objects().only('id').first().id)

    def test_save_history(self):
        s = Scenario(response='bbb')
        u = User()
        s.save()
        u.save()
        self.client.save_history('aaa', s, u.id)
        eq_('aaa', History.objects(scenario__response='bbb').only('request').first().request)

    def test_save_history_scenario_is_none(self):
        u = User()
        u.save()
        self.client.save_history('aaa', None, u.id)
        eq_(None, History.objects(scenario__response='bbb').only('request').first())

    def test_save_history_user_is_none(self):
        s = Scenario(response='bbb')
        self.client.save_history('aaa', s, None)
        eq_('aaa', History.objects(scenario__response='bbb').only('request').first().request)

    @raises(mongoengine.errors.ValidationError)
    def test_save_history_scenario_is_not_allowed_type(self):
        u = User()
        u.save()
        self.client.save_history('aaa', [], u.id)

    def test_save_history_user_is_not_in_db(self):
        s = Scenario(response='bbb')
        u = User()
        s.save()
        self.client.save_history('aaa', s, u.id)
        eq_('aaa', History.objects(scenario__response='bbb').only('request').first().request)
        eq_(None, History.objects(scenario__response='bbb').only('user').first().user)

    def test_import_scenario(self):
        self.client.import_scenario("tests/test_scenario.json")
        eq_(2, Scenario.objects().count())
        eq_("112", Scenario.objects()[1].attributes["id"])
