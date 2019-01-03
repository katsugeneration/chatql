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
        """
        local_values = dict(
            {"request": request},
            **context,
            **self._client.locals)

        for s in self._client.scenarios:
            if eval(s.conditions, local_values):
                return s.response
        return None
