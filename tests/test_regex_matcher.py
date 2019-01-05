# coding=utf-8
#
# Licensed under the MIT License
"""Regex request matcher test code."""
import chatql
from nose.tools import eq_, ok_


class TestRegexMatcher:
    def test_match_is_true(self):
        request = 'hello'
        pattern = r'hello'
        matcher = chatql.matcher.RegexMatcher(request)
        eq_(True, matcher(pattern))

    def test_match_is_false(self):
        request = 'hello'
        pattern = r'hello!'
        matcher = chatql.matcher.RegexMatcher(request)
        eq_(False, matcher(pattern))

    def test_match_case_part(self):
        request = 'hello'
        pattern = r'hell'
        matcher = chatql.matcher.RegexMatcher(request)
        eq_(False, matcher(pattern))

    def test_match_case_part_match(self):
        request = 'hello'
        pattern = r'hell(.*?)'
        matcher = chatql.matcher.RegexMatcher(request)
        eq_(True, matcher(pattern))

    def test_match_case_part_match2(self):
        request = 'hello'
        pattern = r'(.*?)l+(.*?)'
        matcher = chatql.matcher.RegexMatcher(request)
        eq_(True, matcher(pattern))

    def test_match_case_unicode(self):
        request = 'あいうえお'
        pattern = r'(.*?)う(.*?)'
        matcher = chatql.matcher.RegexMatcher(request)
        eq_(True, matcher(pattern))

    def test_match_case_multiline(self):
        request = 'abc\nabc'
        pattern = r'abc(.*?)'
        matcher = chatql.matcher.RegexMatcher(request)
        eq_(True, matcher(pattern))

    def test_match_ignore_case(self):
        request = 'AbC'
        pattern = r'abc'
        matcher = chatql.matcher.RegexMatcher(request)
        eq_(True, matcher(pattern))
