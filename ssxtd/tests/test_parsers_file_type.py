from .. import parsers
from io import BytesIO

def get_virtual_file():
    return BytesIO('''
<animals>
    <i>John</i>
</animals>
'''.encode('utf-8'))

real_file = "ssxtd/tests/t.xml"
gz_file = "ssxtd/tests/t.xml.gz"
zip_file = "ssxtd/tests/t.zip"

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
    f=get_virtual_file()
    d=next(parsers.lxml_parse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_lxml_iterparse_vf():
    f=get_virtual_file()
    d=next(parsers.lxml_iterparse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_lxml_parse_gz():
    f=gz_file
    d=next(parsers.lxml_parse(f, depth=my_depth, compression="gz"))
    assert d == {'i': 'John'}

def test_lxml_iterparse_gz():
    f=gz_file
    d=next(parsers.lxml_iterparse(f, depth=my_depth, compression="gz"))
    assert d == {'i': 'John'}

def test_lxml_parse_zip():
    f=zip_file
    d=next(parsers.lxml_parse(f, depth=my_depth, compression="zip"))
    assert d == {'i': 'John'}

def test_lxml_iterparse_zip():
    f=zip_file
    d=next(parsers.lxml_iterparse(f, depth=my_depth, compression="zip"))
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
    f=get_virtual_file()
    d=next(parsers.xml_parse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_xml_iterparse_vf():
    f=get_virtual_file()
    d=next(parsers.xml_iterparse(f, depth=my_depth, compression=None))
    assert d == {'i': 'John'}

def test_xml_parse_gz():
    f=gz_file
    d=next(parsers.xml_parse(f, depth=my_depth, compression="gz"))
    assert d == {'i': 'John'}

def test_xml_iterparse_gz():
    f=gz_file
    d=next(parsers.xml_iterparse(f, depth=my_depth, compression="gz"))
    assert d == {'i': 'John'}

def test_xml_parse_zip():
    f=zip_file
    d=next(parsers.lxml_parse(f, depth=my_depth, compression="zip"))
    assert d == {'i': 'John'}

def test_xml_iterparse_zip():
    f=zip_file
    d=next(parsers.lxml_iterparse(f, depth=my_depth, compression="zip"))
    assert d == {'i': 'John'}