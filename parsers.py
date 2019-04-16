from semi_structured_xml_to_dict import DictBuilder
from gzip import GzipFile
from zipfile import ZipFile

def get_list_from_tree(my_file, target_depth, tree, ET):
    depth=0
    path=[]
    for event, element in ET.iterparse(my_file,events=("end","start")):
        if event == "start":
            depth+=1
            path.append(element.tag)
        elif event == "end":
            depth-=1
            path = path[:-1]
        if depth == target_depth:
            for i in path:
                tree = tree[i]
            if not isinstance(tree, list):
                tree=[tree]
            return tree
    raise Exception

def get_tag_from_file(my_file, target_depth, ET):
    depth=0
    for event, element in ET.iterparse(my_file,events=("end","start")):
        if event == "start":
            depth+=1
        elif event == "end":
            depth-=1
        if depth == target_depth:
            return element.tag
    raise Exception

    
def dual_generator(filename, compression):
        NO_COMPRESS = None
        GZIP = 'gzip'
        ZIP = 'zip'

        if compression is NO_COMPRESS:  # xml file
            yield filename, filename
        elif compression is GZIP:  # GZIP file
            yield GzipFile(filename), GzipFile(filename)
        elif compression is ZIP:  # ZIP file
            with ZipFile(filename, 'r') as zf:
                for name in zf.namelist():
                    if name.endswith('/'):
                        continue
                    if name.endswith('.xml'):
                        with zf.open(name) as zxml:
                            yield zxml, zxml
                        break

try:
    import xml.etree.ElementTree as OET


    def xml_iterparse(my_file, depth=2,compression=None, object_processor=None):
        for f1 , f2 in dual_generator(my_file, compression):
            tag  = get_tag_from_file(f1, target_depth=depth, ET=OET)

            for event, element in OET.iterparse(f2):
                if element.tag == tag and event == "end":
                    parser = OET.XMLParser(target=DictBuilder(object_processor=object_processor))

                    a = OET.tostring(element)
                    tree = OET.fromstring(a, parser)

                    yield tree[tag]
                    element.clear()

    def xml_parse(my_file, depth=2, compression=None, object_processor=None):
        for f1 , f2 in dual_generator(my_file, compression):
            parser = OET.XMLParser(target=DictBuilder(object_processor=object_processor))
            tree = OET.parse(f1, parser)
            tree = tree.getroot()
            l = get_list_from_tree(f2, target_depth=depth, tree=tree, ET=OET)
            for i in l:
                yield i
except:
    def xml_iterparse(my_file, depth=2, compression=None, object_processor=None):
        print("xml isn't installed : lxml_iterparse is unavailable")

    def xml_parse(my_file, depth=2, compression=None, object_processor=None):
        print("xml isn't installed : lxml_parse is unavailable")      

try:
    from lxml import etree as NET

    def lxml_parse(my_file, depth=2, compression=None, object_processor=None):
        for f1 , f2 in dual_generator(my_file, compression):
            parser = NET.XMLParser(target=DictBuilder(object_processor=object_processor))
            tree = NET.parse(f1, parser)
            l = get_list_from_tree(f2, target_depth=depth, tree=tree, ET=NET)
            for i in l:
                yield i

    def lxml_iterparse(my_file, depth=2, compression=None, object_processor=None):
        for f1 , f2 in dual_generator(my_file, compression):

            #parser = NET.XMLParser(target=DictBuilder(object_processor=object_processor))
            tag  = get_tag_from_file(f1, target_depth=depth, ET=NET)
            for event, element in NET.iterparse(f2, tag=tag):
                parser = NET.XMLParser(target=DictBuilder(object_processor=object_processor))
                a = NET.tostring(element).decode('utf-8')
                tree = NET.fromstring(a, parser)
                yield tree[tag]
                element.clear()
except:
    def lxml_iterparse(my_file, depth=2, compression=None, object_processor=None):
        print("lxml isn't installed : lxml_iterparse is unavailable")

    def lxml_parse(my_file, depth=2, compression=None, object_processor=None):
        print("lxml isn't installed : lxml_parse is unavailable")