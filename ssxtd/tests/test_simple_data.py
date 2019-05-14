import gzip
import zlib
import io
from .. import parsers
from io import BytesIO
import time

text_only_1 = io.BytesIO('''
<animals>
    <i>John</i>
</animals>
'''.encode('utf-8'))

empty_1 = io.BytesIO('''
<animals>
    <i></i>
</animals>
'''.encode('utf-8'))

empty_2 = io.BytesIO('''
<animals>
    <i><text></text></i>
    <i></i>
    <i>solo</i>
</animals>
'''.encode('utf-8'))

self_closing = io.BytesIO('''
<animals>
    <i><text></text></i>
    <i></i>
    <i>solo</i>
</animals>
'''.encode('utf-8'))


my_compression = None



def test_text_only_1():
    f = text_only_1
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': 'John'}}

def test_empty_1():
    f = empty_1
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == None


def test_empty_2():
    f = empty_2
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': 'solo'}}
