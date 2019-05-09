import parsers
from io import BytesIO


schema_test_1 = BytesIO('''
<TankList xmlns="http://www.hmdb.ca">
    <tank><n>Panzer</n></tank>
    <tank><n>Leclerc</n></tank>
</TankList>
'''.encode('utf-8'))

my_depth = 2

def test_lxml_parse():
    f = schema_test_1
    f.seek(0)
    d = next(parsers.lxml_parse(
        f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}

def test_lxml_iterparse():
    f = schema_test_1
    f.seek(0)
    d = next(parsers.lxml_iterparse(f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}

def test_xml_parse():
    f = schema_test_1
    f.seek(0)
    d = next(parsers.xml_parse(
        f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}

def test_xml_iterparse():
    
    f = schema_test_1
    f.seek(0)
    d = next(parsers.xml_iterparse(
        f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}


def test_lxml_parse_cn():
    f = schema_test_1
    f.seek(0)
    d = next(parsers.lxml_parse(
        f, depth=my_depth, compression=None, trim_spaces=True, cleanup_namespaces=False))
    assert d == {'{http://www.hmdb.ca}n': 'Panzer'}

def test_lxml_iterparse_cn():
    f = schema_test_1
    f.seek(0)
    d = next(parsers.lxml_iterparse(
        f, depth=my_depth, compression=None, trim_spaces=True, cleanup_namespaces=False))
    assert d == {'{http://www.hmdb.ca}n': 'Panzer'}

def test_xml_parse_cn():
    f = schema_test_1
    f.seek(0)
    d = next(parsers.xml_parse(
        f, depth=my_depth, compression=None, trim_spaces=True, cleanup_namespaces=False))
    assert d == {'{http://www.hmdb.ca}n': 'Panzer'}

def test_xml_iterparse_cn():
    
    f = schema_test_1
    f.seek(0)
    d = next(parsers.xml_iterparse(
        f, depth=my_depth, compression=None, trim_spaces=True, cleanup_namespaces=False))
    assert d == {'{http://www.hmdb.ca}n': 'Panzer'}

