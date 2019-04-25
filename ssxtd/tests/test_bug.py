import gzip
import zlib
import io
from ssxtd import parsers

import time

semi_structured_xml = io.StringIO('''
<animals> 
    <i species = "lapin" sex = "male" >John</i>
</animals>
''')
my_compression = None


for i in parsers.lxml_parse(semi_structured_xml, depth=2, compression=my_compression):
    print(i)
