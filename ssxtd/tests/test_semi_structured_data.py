import gzip
import zlib
import io
# import parsers
from .. import parsers
from io import BytesIO

import time



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

my_compression = None

def test_semi_structured_xml_1():
    f = semi_structured_xml_1
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin',
                                   '@sex': 'male', '#text': 'John the punisher'}}}


def test_semi_structured_xml_2():
    f = semi_structured_xml_2
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin', '@sex': 'male',
                                   '#text': 'John &\n\tJerry the punisherthe empalor'}}}


def test_semi_structured_xml_3():
    f = semi_structured_xml_3
    d = next(parsers.lxml_parse(f, depth=0, compression=my_compression))
    assert d == {'animals': {'i': {'@species': 'lapin', '@sex': 'male',
                                   '#text': '105 John &\n\tJerry the punisherthe empalor'}}}
