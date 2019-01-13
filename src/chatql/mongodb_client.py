# coding=utf-8
#
# Licensed under the MIT License
"""MongoDB client for ChatQL."""
import mongoengine
import datetime
import json
import functools


class Scenario(mongoengine.Document):
    """Scenario Collection Class."""

    attributes = mongoengine.DictField()
    conditions = mongoengine.StringField()
    response = mongoengine.StringField()
    created_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    modified_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        """Override save method for updating modefied datetime."""
        self.modified_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)

    def to_dict(self):
        """Return dictionary changed object."""
        return {
            "attributes": self.attributes,
            "conditions": self.conditions,
            "response": self.response
        }


class User(mongoengine.DynamicDocument):
    """User Class."""

    def to_dict(self):
        """Return dictionary changed object."""
        ret = {}
        for key in dir(self):
            if key.startswith("_"):
                continue

            if key in ['id', 'objects', 'pk', 'STRICT']:
                continue

            obj = getattr(self, key)
            if callable(obj):
                continue
            ret[key] = obj
        return ret


class History(mongoengine.Document):
    """System Response History Class."""

    request = mongoengine.StringField()
    scenario = mongoengine.DictField()
    user = mongoengine.ReferenceField(User)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class MongoClient(object):
    """MongoDb Client Object."""

    def __init__(self, **config):
        """Mongoclient Constructor."""
        mongoengine.connect(**config)

    @property
    def scenarios(self):
        """Return All Scenario Objects."""
        return Scenario.objects().order_by('-attributes__priority')

    def globals(self, user):
        """Return user usage objects and method."""
        objects = {
            "history": History.objects(user=user),
            "user": User.objects(id=user)
        }

        methods = {
            "isonce": functools.partial(self.isonce, *[user]),
            "last_history": functools.partial(self.last_history, *[user]),
        }
        return dict(
            **objects,
            **methods
        )

    def isonce(self, user, id, period=None):
        """Check scenrio is once in specific period.

        Args:
            user (str): user id used by history filtering
            id (str): scenario id
        Return:
            result (bool): return True case scenario is not in histor, otherwise return False.
        """
        if period is None:
            period_from = datetime.datetime.min
        else:
            period_from = datetime.datetime.utcnow() - period
        return (History.objects(user=user).filter(
                    scenario__attributes__id=id,
                    created_at__gte=period_from).count() == 0)

    def last_history(self, user):
        """Get last history object.

        Args:
            user (str): user id used by history filtering
        Return:
            result (History): return History object when user's history exists, otherwise return None.
        """
        return History.objects(user=user).order_by('-created_at').first()

    def create_new_user(self, **option):
        """Create new user.

        Return:
            ID (str): new user id
        """
        u = User(**option)
        u.save()
        return u

    def get_user_attributes(self, user_id):
        """Get user attributes.

        Args:
            user_id (str): target user id

        Return:
            user (dict): User attributes dictionary. return None, case taget user doesn't exist.
        """
        user = User.objects(id=user_id).first()
        if user is None:
            return None
        return user.to_dict()

    def get_user_id(self, **attributes):
        """Get user id.

        Args:
            atrributes (dict): target user attributes

        Return:
            ID (string): User id. return None, case taget user doesn't exist.
        """
        user = User.objects(**attributes).first()
        if user is None:
            return None
        return user.id

    def save_history(self, request, scenario, user):
        """Save System Response History.

        Args:
            request (str): user input request
            scenario (Scenario or str): response scenario
            user (id): user id. id must need to be user object id in db
        """
        if isinstance(scenario, Scenario):
            s = scenario.to_dict()
        else:
            s = scenario
        h = History(request=request, scenario=s, user=user)
        h.save()
        return h

    def import_scenario(self, path):
        """Import scenario data in DB.

        Args:
            path (str): scenario json data path
        Note:
            data json format is following.
            [
                {
                    "attributes": {
                        "attributes1": "attributes1 value",
                        ...
                    },
                    "conditions": "condition string",
                    "response": "response string"
                },
                ....
            ]
        """
        with open(path, 'r') as f:
            data = json.load(f)

        Scenario.objects().insert([Scenario(**d) for d in data])
