from .. import parsers
from io import BytesIO


schema_test_1 = BytesIO('''
<TankList xmlns="http://www.hmdb.ca">
    <tank><n>Panzer</n></tank>
    <tank><n>Leclerc</n></tank>
</TankList>
'''.encode('utf-8'))

schema_test_2 = BytesIO('''
<TankList xmlns:test="http://www.hmdb.ca">
    <test:tank><n>Panzer</n></test:tank>
    <test:tank><n>Leclerc</n></test:tank>
</TankList>
'''.encode('utf-8'))

my_depth = 2

# FIRST XML
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
    
    f = schema_test_2
    f.seek(0)
    d = next(parsers.xml_iterparse(
        f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}

# SECOND XML
def test_lxml_parse_2():
    f = schema_test_2
    f.seek(0)
    d = next(parsers.lxml_parse(
        f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}

def test_lxml_iterparse_2():
    f = schema_test_2
    f.seek(0)
    d = next(parsers.lxml_iterparse(f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}

def test_xml_parse_2():
    f = schema_test_2
    f.seek(0)
    d = next(parsers.xml_parse(
        f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}

def test_xml_iterparse_2():
    
    f = schema_test_1
    f.seek(0)
    d = next(parsers.xml_iterparse(
        f, depth=my_depth, compression=None, trim_spaces=True))
    assert d == {'n': 'Panzer'}

# FIRST XML WITH cleanup_namespaces=False
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

