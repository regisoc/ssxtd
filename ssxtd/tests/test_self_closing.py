import gzip
import zlib
import io
import parsers
from io import BytesIO
import time

sc_1 = io.BytesIO('''
<animals>
    <i><name value = "Bernard" /></i>
</animals>
'''.encode('utf-8'))



my_compression = None



def test_text_only_1():
    d = next(parsers.lxml_parse(sc_1, depth=2, compression=my_compression))
    print(d)
    assert d == {'name': {'@value': 'Bernard'}}
