# coding=utf-8
#
# Licensed under the MIT License
"""Dialog Management Module."""
from chatql.matcher import RegexMatcher


class DialogEngine(object):
    """Dialog Management Module."""

    def __init__(self, client):
        """Dialogengine Constructor.

        Args:
            client (object): Database access client instance.
        """
        self._client = client

    def generate_response_text(self, request, user=None, **context):
        """Generate Response Text using DB and Intent Estimator.

        Args:
            request (str): user input text
            user (str): (Optional) user specified id.When user is None, system create new user
            context (dict): other values for generating response
        Return:
            response (str): response text. when no response text is None.
        """
        if user is None:
            user = self.create_new_user()

        matcher = {
            "regex": RegexMatcher(request)
        }

        global_values = dict(
            **matcher,
            **context,
            **self._client.globals(user))

        for s in self._client.scenarios:
            conditions = s.conditions.strip()
            if eval(conditions, global_values, {"attributes": s.attributes}):
                return self._client.save_history(request, s, user)
        return self._client.save_history(request, None, user)

    def create_new_user(self, **option):
        """Create new user.

        Args:
            option (sict): Optional attributes dictionary

        Return:
            ID (str): new user id
        """
        return self._client.create_new_user(**option).id

    def get_user_attributes(self, user_id):
        """Get user.

        Args:
            user_id (str): target user id

        Return:
            user (dict): User attributes dictionary. return None, case taget user doesn't exist.
        """
        return self._client.get_user_attributes(user_id)

    def get_user_id(self, **attributes):
        """Get user id.

        Args:
            atrributes (dict): target user attributes

        Return:
            ID (string): User id. return None, case taget user doesn't exist.
        """
        return self._client.get_user_id(**attributes)
