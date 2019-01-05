# coding=utf-8
#
# Licensed under the MIT License
"""Regex request matcher."""
import re


class RegexMatcher(object):
    """Regex request matcher."""

    def __init__(self, request):
        """Regex Matcher Constructor.

        Args:
            request (str): user input request for match
        """
        self._request = request

    def __call__(self, pattern):
        """Match pattern and request.

        Args:
            pattern (str): regex pattern string.
        Return:
            result (bool): match result.
        Note:
            this method calls re.fullmatch
        """
        result = re.fullmatch(pattern, self._request, flags=re.I | re.S)
        return (result is not None)
