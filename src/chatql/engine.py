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
            user_id (str): (Optional) user specified id.When user_id is None, system create new user
            context (dict): other values for generating response
        Return:
            response (str): response text. when no response text is None.
        """
        if user_id is None:
            user_id = self.create_new_user()

        local_values = dict(
            {"request": request},
            **context,
            **self._client.locals(user_id))

        for s in self._client.scenarios:
            conditions = s.conditions.strip()
            if eval(conditions, local_values):
                return self._client.save_history(request, s, user_id)
        return self._client.save_history(request, None, user_id)

    def create_new_user(self):
        """Create new user.

        Return:
            ID (str): new user id
        """
        return self._client.create_new_user().id
