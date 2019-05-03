import parsers
from io import BytesIO

virtual_file = BytesIO('''
<animals>
    <i>John</i>
</animals>
'''.encode('utf-8'))
real_file = "t.xml"
compressed_file = "t.xml.gz"

my_depth = 1


# LXML

def test_lxml_parse_rf():
    f=real_file
    d=next(parsers.lxml_parse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_lxml_iterparse_rf():
    f=real_file
    d=next(parsers.lxml_iterparse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_lxml_parse_vf():
    f=virtual_file
    d=next(parsers.lxml_parse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_lxml_iterparse_vf():
    f=virtual_file
    d=next(parsers.lxml_iterparse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_lxml_parse_gz():
    f=compressed_file
    d=next(parsers.lxml_parse(f, depth=my_depth, compression="gz"))
    assert d == {'i': 'John'}

def test_lxml_iterparse_gz():
    f=compressed_file
    d=next(parsers.lxml_iterparse(f, depth=my_depth, compression="gz"))
    assert d == {'i': 'John'}

# XML

def test_xml_parse_rf():
    f=real_file
    d=next(parsers.xml_parse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_xml_iterparse_rf():
    f=real_file
    d=next(parsers.xml_iterparse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_xml_parse_vf():
    f=virtual_file
    d=next(parsers.xml_parse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_xml_iterparse_vf():
    f=virtual_file
    d=next(parsers.xml_iterparse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_xml_parse_gz():
    f=compressed_file
    d=next(parsers.xml_parse(f, depth=my_depth, compression="gz"))
    assert d == {'i': 'John'}

def test_xml_iterparse_gz():
    f=compressed_file
    d=next(parsers.xml_iterparse(f, depth=my_depth, compression="gz"))
    assert d == {'i': 'John'}

