import gzip
import zlib
import io
from .. import parsers
from io import BytesIO
import time



htmlcode = io.BytesIO('''
<animals>
    <i>John &amp; Jerry</i>
</animals>
'''.encode('utf-8'))


math = io.BytesIO('''
<Abstract>
<AbstractText>We study the simultaneous existence of centres for two families of planar <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML"><mml:msub><mml:mrow><mml:mi>Z</mml:mi></mml:mrow><mml:mi>q</mml:mi></mml:msub></mml:math> -equivariant systems. First, we give a short review about <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML"><mml:msub><mml:mrow><mml:mi>Z</mml:mi></mml:mrow><mml:mi>q</mml:mi></mml:msub></mml:math> -equivariant systems. Next, we present the necessary and sufficient conditions for the simultaneous existence of centres for a <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML"><mml:msub><mml:mrow><mml:mi>Z</mml:mi></mml:mrow><mml:mn>2</mml:mn></mml:msub></mml:math> -equivariant cubic system and for a <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML"><mml:msub><mml:mrow><mml:mi>Z</mml:mi></mml:mrow><mml:mn>2</mml:mn></mml:msub></mml:math> -equivariant quintic system.</AbstractText>
</Abstract>'''.encode('utf-8'))


my_compression = None
my_depth = 2

def test_math():
    f = math
    d = next(parsers.lxml_parse(
        f, depth=0, compression=my_compression, trim_spaces=True))
    print(d)
    assert d == {'Abstract': {'AbstractText': 'We study the simultaneous existence of centres for two families of planarZq-equivariant systems. First, we give a short review aboutZq-equivariant systems. Next, we present the necessary and sufficient conditions for the simultaneous existence of centres for aZ2-equivariant cubic system and for aZ2-equivariant quintic system.'}}



def test_htmlcode_lxml_parse():
    htmlcode.seek(0)
    d = next(parsers.lxml_parse(htmlcode, depth=my_depth, compression=my_compression))
    assert d ==  'John & Jerry'

def test_htmlcode_lxml_iterparse():
    htmlcode.seek(0)
    d = next(parsers.lxml_iterparse(htmlcode, depth=my_depth, compression=my_compression))
    assert d == 'John & Jerry'

def test_htmlcode_xml_parse():
    htmlcode.seek(0)
    d = next(parsers.xml_parse(htmlcode, depth=my_depth, compression=my_compression))
    assert d ==  'John & Jerry'

def test_htmlcode_xml_iterparse():
    htmlcode.seek(0)
    d = next(parsers.xml_iterparse(htmlcode, depth=my_depth, compression=my_compression))
    assert d ==  'John & Jerry'

