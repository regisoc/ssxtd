import xml.etree.ElementTree as OET
from lxml import etree as NET
from semi_structured_xml_to_dict import DictBuilder

def get_list_from_tree(my_file, target_depth, tree, ET=OET):
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
                raise Exception
            return tree
    raise Exception

def get_tag_from_file(my_file, target_depth, ET=OET):
    depth=0
    for event, element in ET.iterparse(my_file,events=("end","start")):
        if event == "start":
            depth+=1
        elif event == "end":
            depth-=1
        if depth == target_depth:
            print(element.tag)
            return element.tag
    raise Exception

def lxml_iterparse(my_file, depth=2):
    parser = NET.XMLParser(target=DictBuilder())
    tag  = get_tag_from_file(my_file, target_depth=depth, ET=NET)
    # for event, element in NET.iterparse(my_file, tag='i'):
    for event, element in NET.iterparse(my_file, tag=tag):
        parser = NET.XMLParser(target=DictBuilder())
        a = NET.tostring(element).decode('utf-8')
        tree = NET.fromstring(a, parser)
        yield tree[tag]
        element.clear()


def xml_iterparse(my_file, depth=2):
    tag  = get_tag_from_file(my_file, target_depth=depth, ET=OET)

    # for event, element in NET.iterparse(my_file, tag='i'):
    for event, element in OET.iterparse(my_file):
        if element.tag == tag and event == "end":
            parser = OET.XMLParser(target=DictBuilder())

            a = OET.tostring(element)
            tree = OET.fromstring(a, parser)

            yield tree[tag]
            element.clear()


def lxml_parse(my_file, depth=2):
    parser = NET.XMLParser(target=DictBuilder())
    tree = NET.parse(my_file, parser)
    l = get_list_from_tree(my_file, target_depth=depth, tree=tree, ET=NET)
    for i in l:
        yield i


def xml_parse(my_file, depth=2):
    parser = OET.XMLParser(target=DictBuilder())
    tree = OET.parse(my_file, parser)
    tree = tree.getroot()
    l = get_list_from_tree(my_file, target_depth=depth, tree=tree, ET=OET)
    for i in l:
        # for i in tree["doc"]["i"]:
        yield i
