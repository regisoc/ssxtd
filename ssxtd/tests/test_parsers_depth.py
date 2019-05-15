from .. import parsers
import pytest

real_file = "ssxtd/tests/t.xml"
my_depth = 0


# LXML

def test_lxml_parse_rf():
    f=real_file
    d=next(parsers.lxml_parse(f, depth=my_depth, compression=None))
    assert d == {'animals': {'i': ['John', 'Jessie']}}

def test_lxml_iterparse_rf():
    with pytest.raises(Exception) as e_info:
        f=real_file
        d=next(parsers.lxml_iterparse(f, depth=my_depth, compression=None))

# XML

def test_xml_parse_rf():
    f=real_file
    d=next(parsers.xml_parse(f, depth=my_depth, compression=None))
    assert d == {'animals': {'i': ['John', 'Jessie']}}

def test_xml_iterparse_rf():
    with pytest.raises(Exception) as e_info:
        f=real_file
        d=next(parsers.xml_iterparse(f, depth=my_depth, compression=None))

