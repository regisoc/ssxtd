import gzip
import zlib
import io
#import parsers
from ssxtd import parsers
from io import BytesIO

import time

text_only_1 = io.BytesIO('''
<animals> 
    <i>John</i>
</animals>
'''.encode('utf-8'))

text_only_2 = io.BytesIO('''
<animals> 
    <i>John &amp; Jerry</i>
</animals>
'''.encode('utf-8'))

attrs_only = io.BytesIO('''
<animals> 
    <i species = "lapin" sex = "male" ></i>
</animals>
'''.encode('utf-8'))

attrs_text_1 = io.BytesIO('''
<animals> 
    <i species = "lapin" sex = "male" >John</i>
</animals>
'''.encode('utf-8'))

attrs_text_2 = io.BytesIO('''
<animals> 
    <i species = "lapin" sex = "male" >John &amp; 
	Jerry</i>
</animals>
'''.encode('utf-8'))

semi_structured_xml_1 = io.BytesIO('''
<animals> 
    <i species = "lapin" sex = "male" >John <aka>the punisher</aka></i>
</animals>
'''.encode('utf-8'))

semi_structured_xml_2 = io.BytesIO('''
<animals> 
    <i species = "lapin" sex = "male" >John &amp; 
	Jerry <aka>the punisher</aka> <aka>the empalor</aka> </i>
</animals>
'''.encode('utf-8'))

semi_structured_xml_3 = io.BytesIO('''
<animals> 
    <i species = "lapin" sex = "male" > <age>105</age> John &amp; 
	Jerry <aka>the punisher</aka> <aka>the empalor</aka> </i>
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

my_compression = None

def test_text_only_1():
    f = text_only_1
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': 'John'}}

def test_text_only_2():
    f = text_only_2
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': 'John & Jerry'}}

def test_attrs_only():
    f = attrs_only
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin', '@sex': 'male'}}}

def test_attrs_text_1():
    f = attrs_text_1
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin', '@sex': 'male', '#text': 'John'}}}

def test_attrs_text_2():
    f = attrs_text_2
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin', '@sex': 'male', '#text': 'John & \n\tJerry'}}}

def test_semi_structured_xml_1():
    f = semi_structured_xml_1
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin', '@sex': 'male', '#text': 'John the punisher'}}}

def test_semi_structured_xml_2():
    f = semi_structured_xml_2
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin', '@sex': 'male', '#text': 'John & \n\tJerry the punisherthe empalor'}}}

def test_semi_structured_xml_3():
    f = semi_structured_xml_3
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin', '@sex': 'male', '#text': '105 John & \n\tJerry the punisherthe empalor'}}}

def test_empty_1():
    f = empty_1
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == None

def test_empty_2():
    f = empty_2
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': 'solo'}}

		

