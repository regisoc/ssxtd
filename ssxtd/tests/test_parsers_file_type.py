from .. import parsers
from io import BytesIO

def get_virtual_file():
    return BytesIO('''
<animals>
    <i>John</i>
    <i>Jessie</i>
</animals>
'''.encode('utf-8'))

real_file = "ssxtd/tests/t.xml"
gz_file = "ssxtd/tests/t.xml.gz"
zip_file = "ssxtd/tests/t.zip"

my_depth = 2


# LXML

def test_lxml_parse_rf():
    f=real_file
    p = parsers.lxml_parse(f, depth=my_depth, compression=None)
    next(p)
    d=next(p)
    assert d == 'Jessie'


def test_lxml_iterparse_rf():
    f=real_file
    p = parsers.lxml_iterparse(f, depth=my_depth, compression=None)
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_lxml_parse_vf():
    f=get_virtual_file()
    p = parsers.lxml_parse(f, depth=my_depth, compression=None)
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_lxml_iterparse_vf():
    f=get_virtual_file()
    p = parsers.lxml_iterparse(f, depth=my_depth, compression=None)
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_lxml_parse_gz():
    f=gz_file
    p = parsers.lxml_parse(f, depth=my_depth, compression="gz")
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_lxml_iterparse_gz():
    f=gz_file
    p = parsers.lxml_iterparse(f, depth=my_depth, compression="gz")
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_lxml_parse_zip():
    f=zip_file
    p = parsers.lxml_parse(f, depth=my_depth, compression="zip")
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_lxml_iterparse_zip():
    f=zip_file
    p = parsers.lxml_iterparse(f, depth=my_depth, compression="zip")
    next(p)
    d=next(p)
    assert d == 'Jessie'

# XML

def test_xml_parse_rf():
    f=real_file
    p = parsers.xml_parse(f, depth=my_depth, compression=None)
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_xml_iterparse_rf():
    f=real_file
    p = parsers.xml_iterparse(f, depth=my_depth, compression=None)
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_xml_parse_vf():
    f=get_virtual_file()
    p = parsers.xml_parse(f, depth=my_depth, compression=None)
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_xml_iterparse_vf():
    f=get_virtual_file()
    p = parsers.xml_iterparse(f, depth=my_depth, compression=None)
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_xml_parse_gz():
    f=gz_file
    p = parsers.xml_parse(f, depth=my_depth, compression="gz")
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_xml_iterparse_gz():
    f=gz_file
    p = parsers.xml_iterparse(f, depth=my_depth, compression="gz")
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_xml_parse_zip():
    f=zip_file
    p = parsers.lxml_parse(f, depth=my_depth, compression="zip")
    next(p)
    d=next(p)
    assert d == 'Jessie'

def test_xml_iterparse_zip():
    f=zip_file
    p = parsers.lxml_iterparse(f, depth=my_depth, compression="zip")
    next(p)
    d=next(p)
    assert d == 'Jessie'

#test_xml_iterparse_rf()