import gzip
import zlib
import io
import parsers
from io import BytesIO
import time

text_only_1 = io.BytesIO('''
<animals>
    <i>John the <b>real</b> chicken</i>
</animals>
'''.encode('utf-8'))




my_compression = None
my_depth = 2


def test_dxml_parse():
    text_only_1.seek(0)
    d = next(parsers.dxml_parse(text_only_1, depth=my_depth, compression=my_compression))
    assert d == 'John the real chicken'

def atest_dxml_iterparse():
    text_only_1.seek(0)
    d = next(parsers.dxml_iterparse(text_only_1, depth=my_depth, compression=my_compression))
    assert d == 'John the real chicken'

#test_dxml_parse()
atest_dxml_iterparse()
