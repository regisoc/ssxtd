import parsers
import pytest
from io import BytesIO

f = BytesIO('''
<animals>
    <i>John</i>
'''.encode('utf-8'))

my_depth = 1


# LXML

def test_lxml_parse():
    d = next(parsers.lxml_parse(f, depth=my_depth, compression=None, recover=True))
    assert d == {'i': 'John'}


def test_lxml_iterparse():
    d = next(parsers.lxml_iterparse(f, depth=my_depth, compression=None, recover=True))
    assert d == {'i': 'John'}
# XML


def test_xml_parse():
    d = next(parsers.xml_parse(f, depth=my_depth, compression=None, recover=True))
    assert d == {'i': 'John'}


def test_xml_iterparse():
    with pytest.raises(Exception) as e_info:
        d = next(parsers.xml_iterparse(f, depth=my_depth, compression=None, recover=True))