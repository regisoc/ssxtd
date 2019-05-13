from semi_structured_xml_to_dict import DictBuilder
from gzip import GzipFile
from zipfile import ZipFile
from bs4 import BeautifulSoup
import io
import re
import copy 
from io import BytesIO
from tqdm import tqdm
import os


def get_list_from_tree(my_file, target_depth, tree, ET, cleanup_namespaces=True, verbose=False):
    """get the list of elements situated at a specific depth
    note  : we could do this with only the tree and not the file, 
            but, to me, it seemed clearer this way, because share the same algo as get_tag_from_file, 
            which cannot parse the tree, as it hasn't been created
    
    Arguments:
        my_file {string} -- the file to be parsed so we can get the path of the element of the required depth
        target_depth {int} -- depth of the elements
        tree {dict} -- dict from which the list is extracted
        ET {library} -- library used to parse
    
    Raises:
        Exception: no elements found at the required depth 
    
    Returns:
        [list] -- list of the elements
    """
    depth=0
    path=[]
    if isinstance ( my_file, io.BytesIO):
        my_file.seek(0)
    for event, element in ET.iterparse(my_file,events=("end","start")):
        if cleanup_namespaces:
            tag = re.sub('{.*}', '', element.tag)
        else:
            tag = element.tag
        if event == "start":
            depth+=1
            path.append(tag)
        elif event == "end":
            depth-=1
            path = path[:-1]
        if depth == target_depth:
            for i in path:
                
                try:
                    tree = tree[i]
                except:
                    return [None]
            if not isinstance(tree, list):
                tree=[tree]
            return tree
    raise Exception ("no elements found at the required depth")

def get_tag_from_file(my_file, target_depth, ET):
    """get the tag's name at the required depth
    
    Arguments:
        my_file {string} -- file to be parsed
        target_depth {int} -- depth of the tag
        ET {library} -- library used to parse
    
    Raises:
        Exception: no elements found at the required depth
    
    Returns:
        string -- tag name
    """
    depth=0
    if isinstance ( my_file, io.BytesIO):
        my_file.seek(0)
    for event, element in ET.iterparse(my_file,events=("end","start")):
        if event == "start":
            depth+=1
        elif event == "end":
            depth-=1
        if depth == target_depth:
            return element.tag
    raise Exception("no elements found at the required depth")


    
def file_generator(filename, compression):
    """return readable files, return 2x the same file because we need to parse 2 times and ZipFile can't support seek(0)
    
    Arguments:
        filename {string} -- file to parse
        compression {string} -- file type
    """
    NO_COMPRESS = None
    GZIP = 'gz'
    ZIP = 'zip'

    if compression is NO_COMPRESS:  # xml file
        if isinstance(filename, str):
            yield open(filename, "rb"), open(filename, "rb")
        else:
            yield filename, filename
    elif compression is GZIP:  # GZIP file
        yield GzipFile(filename), GzipFile(filename)
    elif compression is ZIP:  # ZIP file
        with ZipFile(filename, 'r') as zf:
            for name in zf.namelist():
                if name.endswith('/'):
                    continue
                if name.endswith('.xml'):
                    yield zf.open(name), zf.open(name)


### XML
try:
    import xml.etree.ElementTree as OET


    def xml_iterparse(my_file, depth=2,compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False):
        """parse by iteration, can't recover on bad XML
        
        Arguments:
            my_file {[type]} -- [description]
        
        Keyword Arguments:
            depth {int} -- [description] (default: {2})
            compression {[type]} -- [description] (default: {None})
            value_processor {[type]} -- [description] (default: {None})
            object_processor {[type]} -- [description] (default: {None})
            trim_spaces {bool} -- [description] (default: {False})
            del_empty {bool} -- [description] (default: {True})
        
        Raises:
            Exception: [description]
        """
        if depth == 0:
            raise Exception ("Depth must be > 0 for iterparse")
        for f1, f2  in file_generator(my_file, compression):
            tag  = get_tag_from_file(f1, target_depth=depth, ET=OET)
            if isinstance(f1, (io.BytesIO, GzipFile, io.BufferedReader)):
                f1.seek(0, os.SEEK_END)
                file_size = f1.tell()
                f1.seek(0) 
            else:
                file_size = os.stat(f1).st_size
            if cleanup_namespaces:
                cleaned_tag = re.sub('{.*}', '', tag)
            else:
                cleaned_tag = tag
            if verbose:
                old_position = 0
                pbar = tqdm(total=file_size, unit_scale=True, unit="bytes")
            for _, element in OET.iterparse(f2):
                if element.tag == tag:
                    parser = OET.XMLParser(target=DictBuilder(value_processor=value_processor, object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces))

                    a = OET.tostring(element)
                    tree = OET.fromstring(a, parser)

                    yield tree[cleaned_tag]
                    element.clear()
                    if verbose:
                        pbar.update(f2.tell()-old_position)
                        old_position = f2.tell()
            if verbose:
                pbar.close()

    def xml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        for f1, f2  in file_generator(my_file, compression):
            parser = OET.XMLParser(target=DictBuilder(value_processor=value_processor, object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces))
            if isinstance(f1, (io.BytesIO, GzipFile, io.BufferedReader)):
                f1.seek(0, os.SEEK_END)
                file_size = f1.tell()
                f1.seek(0) 
            else:
                file_size = os.stat(f1).st_size
            if recover:
                f1 = io.BytesIO(BeautifulSoup(f1, "html.parser").encode('utf-8'))
            if verbose:
                pbar = tqdm(total=file_size, unit_scale=True, unit="bytes")
            #tree = OET.parse(f1, parser)
            while True:
                data = f1.read(65536)
                parser.feed(data)
                if not data:
                    break
                elif verbose:
                    pbar.update(65536)
            tree = parser.close()
            if verbose:
                pbar.close()
            if isinstance(f1, (io.BytesIO, GzipFile)):
                            f1.seek(0)
            #tree = tree.getroot()
            l = get_list_from_tree(f2, target_depth=depth, tree=tree, ET=OET, cleanup_namespaces=cleanup_namespaces)
            if verbose:
                print("finished parsing, serving")
            for i in l:
                yield i
            
except:
    def xml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("xml isn't installed : xml_iterparse is unavailable")

    def xml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("xml isn't installed : xml_parse is unavailable")      

## DEFUSE XML

try:
    import defusedxml.ElementTree as DET


    def dxml_iterparse(my_file, depth=2,compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False):
        """parse by iteration, can't recover on bad XML
        
        Arguments:
            my_file {[type]} -- [description]
        
        Keyword Arguments:
            depth {int} -- [description] (default: {2})
            compression {[type]} -- [description] (default: {None})
            value_processor {[type]} -- [description] (default: {None})
            object_processor {[type]} -- [description] (default: {None})
            trim_spaces {bool} -- [description] (default: {False})
            del_empty {bool} -- [description] (default: {True})
        
        Raises:
            Exception: [description]
        """
        if depth == 0:
            raise Exception ("Depth must be > 0 for iterparse")
        for f1, f2  in file_generator(my_file, compression):
            tag  = get_tag_from_file(f1, target_depth=depth, ET=DET)
            if isinstance(f1, (io.BytesIO, GzipFile)):
                f1.seek(0)
            if cleanup_namespaces:
                cleaned_tag = re.sub('{.*}', '', tag)
            else:
                cleaned_tag = tag
            for event, element in DET.iterparse(f2):
                if element.tag == tag:
                    parser = DET.XMLParser(target=DictBuilder(value_processor=value_processor, object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces))

                    a = DET.tostring(element)
                    b = BytesIO(a)
                    tree = DET.parse(b, parser)
                    root = tree.getroot()
                    yield root[cleaned_tag]
                    element.clear()

    def dxml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        for f1, f2  in file_generator(my_file, compression):
            parser = DET.XMLParser(target=DictBuilder(value_processor=value_processor, object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces))
            if isinstance(f1, (io.BytesIO, GzipFile)):
                f1.seek(0)
            if recover:
                f1 = io.BytesIO(BeautifulSoup(f1, "html.parser").encode('utf-8'))
            tree = DET.parse(f1, parser)
            if isinstance(f1, (io.BytesIO, GzipFile)):
                            f1.seek(0)
            tree = tree.getroot()
            l = get_list_from_tree(f2, target_depth=depth, tree=tree, ET=DET, cleanup_namespaces=cleanup_namespaces)
            for i in l:
                yield i
except:
    def dxml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("xml isn't installed : xml_iterparse is unavailable")

    def dxml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("xml isn't installed : xml_parse is unavailable")      


## LXML
try:
    from lxml import etree as NET

    def lxml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        for f1, f2  in file_generator(my_file, compression):
            parser = NET.XMLParser(recover=recover, target=DictBuilder(value_processor=value_processor, object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces))
            tree = NET.parse(f1, parser)
            if isinstance(f1, (io.BytesIO, GzipFile)):
                f1.seek(0)
            l = get_list_from_tree(f2, target_depth=depth, tree=tree, ET=NET, cleanup_namespaces=cleanup_namespaces)
            for i in l:
                yield i

    def lxml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        if depth == 0:
            raise Exception ("Depth must be > 0 for iterparse")
        for f1, f2  in file_generator(my_file, compression):
            #parser = NET.XMLParser(target=DictBuilder(value_processor=value_processor, object_processor=object_processor))
            tag  = get_tag_from_file(f1, target_depth=depth, ET=NET)
            if isinstance(f1, (io.BytesIO, GzipFile)):
                f1.seek(0)

            if cleanup_namespaces:
                cleaned_tag = re.sub('{.*}', '', tag)
            else:
                cleaned_tag = tag
            # TODO : make an element parser so tostring isn't needed anymore
            for event, element in NET.iterparse(f2, tag=tag, recover=recover):
                parser = NET.XMLParser(recover=recover, target=DictBuilder(value_processor=value_processor, object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces))
                a = NET.tostring(element).decode('utf-8')
                tree = NET.fromstring(a, parser)
                yield tree[cleaned_tag]
                element.clear()

            
except:
    def lxml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("lxml isn't installed : lxml_iterparse is unavailable")

    def lxml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("lxml isn't installed : lxml_parse is unavailable")

