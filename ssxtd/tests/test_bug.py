import gzip
import zlib
import io
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

files = [text_only_1, text_only_2, attrs_only, attrs_text_1, attrs_text_2, semi_structured_xml_1, semi_structured_xml_2, semi_structured_xml_3]
my_compression = None

for f in files:
    for i in parsers.lxml_parse(f, depth=2, compression=my_compression):
        print(i)
		
