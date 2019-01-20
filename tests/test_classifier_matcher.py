# coding=utf-8
#
# Licensed under the MIT License
"""Regex request matcher test code."""
import chatql
import os
from nose.tools import eq_, ok_


def test_download_model_file():
    ok_(os.path.exists("/tmp/chatql/bert_pretrained_model"))
    ok_(os.path.exists("/tmp/chatql/bert_pretrained_model/multi_cased_L-12_H-768_A-12/bert_config.json"))
    ok_(os.path.exists("/tmp/chatql/bert_pretrained_model/multi_cased_L-12_H-768_A-12/vocab.txt"))
    ok_(os.path.exists("/tmp/chatql/bert_pretrained_model/multi_cased_L-12_H-768_A-12/bert_model.ckpt.index"))


class TestClassifierMatcher:
    def test_init(self):
        pass
