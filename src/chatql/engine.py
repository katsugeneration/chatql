# coding=utf-8
#
# Licensed under the MIT License
"""Dialog Management Module."""


class DialogEngine(object):
    """Dialog Management Module."""

    def __init__(self, client):
        """Dialogengine Constructor.

        Args:
            client (object): Database access client instance.
        """
        self._client = client

    def generate_response_text(self, request, user_id=None, **context):
        """Generate Response Text using DB and Intent Estimator.

        Args:
            request (str): user input text
            user_id (str): (Optional) user specified id
            context (dict): other values for generating response
        Return:
            response (str): response text. when no response text is None.
        """
        local_values = dict(
            {"request": request},
            **context,
            **self._client.locals(user_id))

        for s in self._client.scenarios:
            conditions = s.conditions.strip()
            if eval(conditions, local_values):
                return s.response
        return None

    def create_new_user(self):
        """Create new user.

        Return:
            ID (str): new user id
        """
        return self._client.create_new_user().id
