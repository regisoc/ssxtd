class DictBuilder:
    """Generic element structure builder.
    This builder converts a sequence of start, data, and end method
    calls to a well-formed element structure.
    You can use this class to build an element structure using a custom XML
    parser, or a parser for some other XML-like format.
    *element_factory* is an optional element factory which is called
    to create new Element instances, as necessary.
    """
    def __init__(self, trim_spaces=False, to_int = True, to_float=True):
        self.dict = {}
        self.path = []
        self.leaf = {}
        self.trim_spaces = trim_spaces
        self.to_int = to_int
        self.to_float = to_float


    def getLeaf(self):

        leaf=self.dict
        for i in self.path:
            l=leaf["#alldata"]
            le=l[-1]
            leaf=le[i]
        
        return leaf

    def getParentLeaf(self):
        leaf=self.dict
        for i in self.path[:-1]:
            l=leaf["#alldata"]
            le=l[-1]
            leaf=le[i]
        
        return leaf

    def remove_tag_all_data(self,d):

        if isinstance(d, list):
            for i in d:
                self.remove_tag_all_data(i)
        elif isinstance(d, str):
            return
        elif isinstance(d, dict):
            d.pop("#alldata", None)
            
            for i in d:
                self.remove_tag_all_data(i)
            


    def close(self):
        root = self.dict["#alldata"][0]
        self.clean(root)
        return root


    def data(self, data):
        if data.isspace():
            return
        if self.trim_spaces:
            data=" ".join(data.split())
        self.leaf = self.getLeaf()
        self.leaf["#alldata"].append(data)

        

    def start(self, tag, attrs):
        #print(self.dict)
        self.leaf = self.getLeaf()
        if self.leaf.get("#alldata") is None:
            self.leaf["#alldata"]=[]

        new_tag = {tag: {"#alldata": []}}
        for k,v in attrs.items():
            new_tag[tag]["@"+k]=v

        self.leaf["#alldata"].append(new_tag)
  
        
        

        self.path.append(tag)

    def merge_tag_text(self, o):
        r=""
        if isinstance(o, list):
            for i in o:
                r=r+self.merge_tag_text(i)
        elif isinstance(o, str):
            r=r+o
        elif isinstance(o, dict):
            if o.get("#alldata") is None:
                for v in o.values():
                    r=r+self.merge_tag_text(v)
            else:
                r=r+self.merge_tag_text(o["#alldata"])
        return r

    def add_tag(self, d, k, v):
        t=d.get(k)

        if t is None:
            d[k]=v
        elif isinstance(t, (str, dict)):
            d[k] = [d[k],v]
        elif isinstance(t, list):
            t.append(v)

        

    def merge_tag(self, l):
        """[summary]
        
        Arguments:
            l {[type]} -- [{'content1': ...}, {'content2': ...}]
        """
        r={}

        for i in l:
            # i : 'content1': ...
            self.clean(i)
            for k, v in i.items():
                self.add_tag(r, k,v)

        return r
        
    def clean(self, d ):
        '''[summary]
        
        Arguments:
            d {[type]} -- {'i': {'#alldata': [{'content1': {'#alldata': ...}, {'content2': {'#alldata': ...},'oui']}}}
        '''
        
        k = next(iter(d)) # k='i'

        has_attrs=False
        for i in d[k]:
            if i != "#alldata":
                has_attrs=True
        l = d[k]["#alldata"]#[{'content1': {'#alldata': ...}, {'content2': {'#alldata': ...},'oui']
        
        
        n_tag=0
        n_text=0
        
        for i in l:
            if isinstance(i, dict):
                n_tag+=1
            elif isinstance(i, str):
                n_text+=1

        if n_text == 1 and n_tag == 0: # if ['oui']
            if has_attrs:
                d[k]["#text"]=l[0]
                d[k].pop("#alldata", None)
            else:
                r = self.try_conversion(l[0])
                d[k]=r
        
        elif n_tag != 0 and n_text ==0: # if [{'content1': {'#alldata': ...}}, {'content2': {'#alldata': ...}}]
            if has_attrs:
                for key,val in d[k].items():
                    if key != "#alldata":
                        l.append({key:  {'#alldata': [val]}})
            d[k]=self.merge_tag(l)

        elif n_tag != 0 and n_text !=0: # if [{'content1': {'#alldata': ...},'oui']
            if has_attrs:
                d[k]["#text"]=self.merge_tag_text(l)
            else:
                d[k]=self.merge_tag_text(l)
            
    def try_conversion(self, value):
        if self.to_int:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass
        if self.to_float:
            try:
                return float(value)
            except (ValueError, TypeError):
                pass
        return value        


    def end(self, tag):
        del self.path[-1]
