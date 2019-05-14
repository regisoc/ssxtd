from semi_structured_xml_to_dict import DictBuilder
from gzip import GzipFile
from zipfile import ZipFile, ZipExtFile
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
    depth = 0
    path = []
    if isinstance(my_file, io.BytesIO):
        my_file.seek(0)
    for event, element in ET.iterparse(my_file, events=("end", "start")):
        if cleanup_namespaces:
            tag = re.sub('{.*}', '', element.tag)
        else:
            tag = element.tag
        if event == "start":
            depth += 1
            path.append(tag)
        elif event == "end":
            depth -= 1
            path = path[:-1]
        if depth == target_depth:
            for i in path:

                try:
                    tree = tree[i]
                except:
                    return [None]
            if not isinstance(tree, list):
                tree = [tree]
            return tree
    raise Exception("no elements found at the required depth")


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
    depth = 0
    if isinstance(my_file, io.BytesIO):
        my_file.seek(0)
    for event, element in ET.iterparse(my_file, events=("end", "start")):
        if event == "start":
            depth += 1
        elif event == "end":
            depth -= 1
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
                    yield zf.open(name, mode='r'), zf.open(name, mode='r')


# XML
try:
    import xml.etree.ElementTree as OET

    def xml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False):
        pm = XML_IterParser_Manager(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor,
                                    object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose)
        yield from pm.run()

    def xml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        pm = XML_SimpleParser_Manager(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor, object_processor=object_processor,
                                      trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        yield from pm.run()


except:
    def xml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("xml isn't installed : xml_iterparse is unavailable")

    def xml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("xml isn't installed : xml_parse is unavailable")

# DEFUSE XML

try:
    import defusedxml.ElementTree as DET

    def dxml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False):
        pm = DXML_IterParser_Manager(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor,
                                     object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose)
        yield from pm.run()

    def dxml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        pm = DXML_SimpleParser_Manager(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor,
                                       object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose)
        yield from pm.run()

except:
    def dxml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("defusedxml isn't installed : dxml_iterparse is unavailable")

    def dxml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("defusedxml isn't installed : dxml_parse is unavailable")

# LXML
try:
    from lxml import etree as NET

    def lxml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        pm = LXML_SimpleParser_Manager(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor,
                                       object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        yield from pm.run()


    def lxml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        pm = LXML_IterParser_Manager(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor,
                                       object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        yield from pm.run()
        


except:
    def lxml_iterparse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("lxml isn't installed : lxml_iterparse is unavailable")

    def lxml_parse(my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        print("lxml isn't installed : lxml_parse is unavailable")


class Parser_Manager:

    ITER = "iter"
    SIMPLE = "simple"

    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        self.my_file = my_file
        self.depth = depth
        self.compression = compression
        self.value_processor = value_processor
        self.object_processor = object_processor
        self.trim_spaces = trim_spaces
        self.del_empty = del_empty
        self.cleanup_namespaces = cleanup_namespaces
        self.verbose = verbose
        self.recover = recover

        self.old_position = 0

        self.type = ""
        self.lib = None
        self.tag = ""
        self.f1 = None
        self.f2 = None
        self.file_size = None
        self.cleaned_tag = ""
        self.pbar = None

    def check_depth(self):
        if self.depth == 0 and self.type == Parser_Manager.ITER:
            raise Exception("Depth must be > 0 for iterparse")

    def set_tag(self):
        self.tag = get_tag_from_file(self.f1, target_depth=self.depth, ET=self.lib)

    def set_size(self):
        if isinstance(self.f1, (io.BytesIO, GzipFile, io.BufferedReader, ZipExtFile)):
            self.f1.seek(0, os.SEEK_END)
            self.file_size = self.f1.tell()
            self.f1.seek(0)
        else:
            print("should not happend")
            self.file_size = os.stat(self.f1).st_size

    def set_cleaned_tag(self):
        if self.cleanup_namespaces:
            self.cleaned_tag = re.sub('{.*}', '', self.tag)
        else:
            self.cleaned_tag = self.tag

    def create_pbar(self):
        if self.verbose:
            self.pbar = tqdm(total=self.file_size,
                             unit_scale=True, unit="bytes")

    def close_pbar(self):
        if self.verbose:
            self.pbar.close()



    def run(self):
        raise Exception("run need an implementation")

    def parse(self):
        raise Exception("run need an implementation")


class IterParser_Manager (Parser_Manager):
    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        super().__init__(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor,
                         object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        self.type = Parser_Manager.ITER

    def run(self):
        self.check_depth()
        for f1, f2 in file_generator(self.my_file, self.compression):
            self.f1 = f1
            self.f2 = f2
            self.set_tag()
            self.set_size()
            self.set_cleaned_tag()
            self.create_pbar
            yield from self.parse()
            self.close_pbar()

    def parse(self):
        bd = DictBuilder(value_processor=self.value_processor, object_processor=self.object_processor,
                                                       trim_spaces=self.trim_spaces, del_empty=self.del_empty, cleanup_namespaces=self.cleanup_namespaces)
        self.parser = self.lib.XMLParser(target=bd)
        
        for _, element in self.lib.iterparse(self.f2):
            yield from self.process(element)

            
    def process(self, element):
        if element.tag == self.tag:
            a = self.lib.tostring(element)

            # Solution1 -> ne marche pas pour defusedxml car le parser de fromstring n'est pas pris en compte
            #root = self.lib.fromstring(a, parser)

            # Solution 2
            b = BytesIO(a)
            tree = self.lib.parse(b, self.parser)
            if self.lib == OET or self.lib == DET:
                root = tree.getroot()
            elif self.lib == NET:
                root = tree

            yield root[self.cleaned_tag]
            element.clear()
            self.update_pbar()
        
    def update_pbar(self):
        if self.verbose:
            self.pbar.update(self.f2.tell()-self.old_position)
            self.old_position = self.f2.tell()

class SimpleParser_Manager (Parser_Manager):
    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        super().__init__(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor, object_processor=object_processor,
                         trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        self.type = Parser_Manager.SIMPLE

    def parse(self):
        parser = self.lib.XMLParser(target=DictBuilder(value_processor=self.value_processor, object_processor=self.object_processor,
                                                       trim_spaces=self.trim_spaces, del_empty=self.del_empty, cleanup_namespaces=self.cleanup_namespaces))

        while True:
            data = self.f1.read(65536)
            parser.feed(data)
            if not data:
                break
            elif self.verbose:
                self.pbar.update(65536)
        return parser.close()

    def run(self):
        self.check_depth()
        for f1, f2 in file_generator(self.my_file, self.compression):
            self.f1 = f1
            self.f2 = f2
            self.set_size()
            if self.recover:
                self.f1 = io.BytesIO(BeautifulSoup(
                    self.f1, "html.parser").encode('utf-8'))
            self.create_pbar
            tree = self.parse()
            self.close_pbar()
            if isinstance(self.f1, (io.BytesIO, GzipFile)):
                self.f1.seek(0)
            l = get_list_from_tree(f2, target_depth=self.depth, tree=tree,
                                   ET=OET, cleanup_namespaces=self.cleanup_namespaces)
            if self.verbose:
                print("finished parsing, serving")
            for i in l:
                yield i





class XML_SimpleParser_Manager (SimpleParser_Manager):
    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        super().__init__(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor, object_processor=object_processor,
                         trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        self.lib = OET

class XML_IterParser_Manager (IterParser_Manager):
    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        super().__init__(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor, object_processor=object_processor,
                         trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        self.lib = OET


class DXML_SimpleParser_Manager (SimpleParser_Manager):
    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        super().__init__(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor, object_processor=object_processor,
                         trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        self.lib = DET

class DXML_IterParser_Manager (IterParser_Manager):
    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False):
        super().__init__(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor,
                         object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose)
        self.lib = DET

class LXML_SimpleParser_Manager (SimpleParser_Manager):
    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        super().__init__(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor, object_processor=object_processor,
                         trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        self.lib = NET

class LXML_IterParser_Manager (IterParser_Manager):
    def __init__(self, my_file, depth=2, compression=None, value_processor=None, object_processor=None, trim_spaces=False, del_empty=True, cleanup_namespaces=True, verbose=False, recover=False):
        super().__init__(my_file=my_file, depth=depth, compression=compression, value_processor=value_processor,
                         object_processor=object_processor, trim_spaces=trim_spaces, del_empty=del_empty, cleanup_namespaces=cleanup_namespaces, verbose=verbose, recover=recover)
        self.lib = NET

    def parse(self):
        bd = DictBuilder(value_processor=self.value_processor, object_processor=self.object_processor,
                                                       trim_spaces=self.trim_spaces, del_empty=self.del_empty, cleanup_namespaces=self.cleanup_namespaces)

        self.parser = self.lib.XMLParser(recover=self.recover, target=bd)
        
        for _, element in self.lib.iterparse(self.f2, recover=self.recover):
            
            yield from self.process(element)