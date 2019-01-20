# coding=utf-8
#
# Licensed under the MIT License
"""Dialog Management Module."""
import os
from chatql.matcher import RegexMatcher, ClassifierMatcher


class DialogEngine(object):
    """Dialog Management Module."""

    def __init__(self, client):
        """Dialogengine Constructor.

        Args:
            client (object): Database access client instance.
        """
        self._client = client
        self._classifier_matcher = ClassifierMatcher()

    def train_matcher(self, model_dir):
        """Train matcher.

        Args:
            model_dir: model saved directory path.
        """
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        intents = self._client.get_intent(intent_type='classifier')
        outputs = []
        for intent in intents:
            outputs.extend([[intent.name, i] for i in intent.intents])
        label_list = sorted([str(i.name) for i in intents])
        with open(os.path.join(model_dir, "train.tsv"), 'w') as f:
            for o in outputs:
                f.write(o[0] + "\t" + o[1] + "\n")

        self._classifier_matcher.load_model(
            model_dir,
            label_list,
            len(outputs)
        )
        self._classifier_matcher.train(model_dir)

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
