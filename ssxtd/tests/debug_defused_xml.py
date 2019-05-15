from ..semi_structured_xml_to_dict import DictBuilder
import defusedxml.ElementTree as DET
from io import BytesIO

a = b'<animals><i>John the <b>real</b> chicken</i><i>John the <b>real</b> chicken</i></animals>\n'
parser = DET.XMLParser(target=DictBuilder())
root = DET.fromstring(a, parser)
print(type(root))

b = BytesIO('''
<animals><i>John the <b>real</b> chicken</i></animals>
'''.encode('utf-8'))

parser = DET.XMLParser(target=DictBuilder())
tree = DET.parse(b, parser)
root = tree.getroot()
print(type(root))
