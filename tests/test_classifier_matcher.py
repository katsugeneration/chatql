# coding=utf-8
#
# Licensed under the MIT License
"""Regex request matcher test code."""
import chatql
import os
import shutil
from nose.tools import eq_, ok_


def test_download_model_file():
    ok_(os.path.exists("/tmp/chatql/bert_pretrained_model"))
    ok_(os.path.exists("/tmp/chatql/bert_pretrained_model/multi_cased_L-12_H-768_A-12/bert_config.json"))
    ok_(os.path.exists("/tmp/chatql/bert_pretrained_model/multi_cased_L-12_H-768_A-12/vocab.txt"))
    ok_(os.path.exists("/tmp/chatql/bert_pretrained_model/multi_cased_L-12_H-768_A-12/bert_model.ckpt.index"))


class TestClassifierMatcher:
    def test_train(self):
        matcher = chatql.matcher.ClassifierMatcher()
        matcher.load_model(
            "classifier_test_model",
            ["0", "1"],
            14
        )
        matcher.train(os.path.join(os.path.dirname(__file__), "classifier_test"))
        ok_(os.path.exists("classifier_test_model/checkpoint"))
        shutil.rmtree("classifier_test_model", ignore_errors=True)

    def test_predict(self):
        matcher = chatql.matcher.ClassifierMatcher()
        matcher.load_model(
            "classifier_test_model",
            ["0", "1"],
            14
        )
        matcher.train(os.path.join(os.path.dirname(__file__), "classifier_test"))
        matcher.request = "それはやめましょう。"
        ret = matcher(1)
        shutil.rmtree("classifier_test_model", ignore_errors=True)
        ok_(ret)
