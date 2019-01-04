# coding=utf-8
#
# Licensed under the MIT License
"""MongoDB client for ChatQL."""
import mongoengine
import datetime
import json


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

    pass


class History(mongoengine.Document):
    """System Response History Class."""

    request = mongoengine.StringField()
    scenario = mongoengine.DictField()
    user_id = mongoengine.ReferenceField(User)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)


class MongoClient(object):
    """MongoDb Client Object."""

    def __init__(self, **config):
        """Mongoclient Constructor."""
        mongoengine.connect(**config)

    @property
    def scenarios(self):
        return Scenario.objects()

    def locals(self, user_id):
        return {
            "history": History.objects(user_id=user_id),
            "user": User.objects(id=user_id)}

    def create_new_user(self):
        """Create new user.

        Return:
            ID (str): new user id
        """
        u = User()
        u.save()
        return u.id

    def save_history(self, request, scenario, user_id):
        """Save System Response History.
        
        Args:
            request (str): user input request
            scenario (Scenario or str): response scenario
            user_id (id): user id. id must need to be user object id in db
        """
        if isinstance(scenario, Scenario):
            s = scenario.to_dict()
        else:
            s = scenario
        h = History(request=request, scenario=s, user_id=user_id)
        h.save()

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
