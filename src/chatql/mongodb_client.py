# coding=utf-8
#
# Licensed under the MIT License
"""MongoDB client for ChatQL."""
import mongoengine
import datetime


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


class User(mongoengine.DynamicDocument):
    """User Class."""

    pass


class History(mongoengine.Document):
    """System Response History Class."""

    request = mongoengine.StringField()
    scenario = mongoengine.DictField(required=True)
    user_id = mongoengine.ReferenceField(User, required=True)
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
