import parsers
import pytest
from io import BytesIO

f1 = BytesIO('''
<animals>
    <i>John</i>
'''.encode('utf-8'))

my_depth = 1


# LXML

def test_lxml_parse():
    f1.seek(0)
    d = next(parsers.lxml_parse(f1, depth=my_depth, compression=None, recover=True, trim_spaces=True))
    assert d == {'i': 'John'}


def test_lxml_iterparse():
    f1.seek(0)
    d = next(parsers.lxml_iterparse(f1, depth=my_depth, compression=None, recover=True, trim_spaces=True))
    assert d == {'i': 'John'}
# XML


def test_xml_parse():
    f1.seek(0)
    d = next(parsers.xml_parse(f1, depth=my_depth, compression=None, recover=True))
    assert d == {'i': 'John'}


def test_xml_iterparse():
    f1.seek(0)
    with pytest.raises(Exception) as e_info:
        d = next(parsers.xml_iterparse(f, depth=my_depth, compression=None, recover=True))

f2 = BytesIO('''
<animals>
    <i>John
'''.encode('utf-8'))

my_depth = 1


# LXML

def test_lxml_parse_2():
    f2.seek(0)
    d = next(parsers.lxml_parse(f2, depth=my_depth, compression=None, recover=True, trim_spaces=True))
    assert d == {'i': 'John'}


def test_lxml_iterparse_2():
    f2.seek(0)
    d = next(parsers.lxml_iterparse(f2, depth=my_depth, compression=None, recover=True, trim_spaces=True))
    assert d == {'i': 'John'}


# XML
def test_xml_parse_2():
    f2.seek(0)
    d = next(parsers.xml_parse(f2, depth=my_depth, compression=None, recover=True, trim_spaces=True))
    assert d == {'i': 'John'}


def test_xml_iterparse_2():
    f2.seek(0)
    with pytest.raises(Exception) as e_info:
        d = next(parsers.xml_iterparse(f2, depth=my_depth, compression=None, recover=True, trim_spaces=True ))


