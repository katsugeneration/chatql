import chatql
from chatql import __version__
from nose.tools import eq_


def test_version():
    assert __version__ == '0.1.0'


class TestQL:
    def queryHelloTest(self):
        query = '''
            query SayHello {
            hello
            }
        '''
        result = chatql.ql.schema.execute(query)
        eq_(result, 'hello World')