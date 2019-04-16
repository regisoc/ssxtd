from xml_file_reader import XMLFileReader
import gzip
import zlib
#from collections import defaultdict
from parsers import *

import time

my_file = "exemple.xml"

my_compression=None

#[{'month': {'#alldata': ['09']}}, {'year': {'#alldata': ['1993']}}, {'jour': {'#alldata': ['09']}}]
def ip(path, k):
        l=k['#alldata']
        month=None
        year=None
        day=None
        if len(l) == 3:
                # it should always be a dict with one key, and a subdict as value, containing  an "#alldata" key
                # {'month': {'#alldata': ['09']}}
                for i in l:
                        # month
                        k = next(iter(i))
                        # ['09']
                        ad = i[k]['#alldata']
                        if k == "month" and len(ad) == 1 and isinstance (ad[0], str):
                                month=ad[0]
                        elif k == "year" and len(ad) == 1 and isinstance (ad[0], str):
                                year=ad[0]
                        elif k == "day" and len(ad) == 1 and isinstance (ad[0], str):
                                day=ad[0]
                if month is not None and year is not None and day is not None:
                        r=year+"-"+month+"-"+day
                        return r
        return None

        

def xmltodict(compression):
    if compression=="gzip":
        yield from XMLFileReader(my_file,compression=XMLFileReader.GZIP,  to_int=False).read()
    else:         
        yield from XMLFileReader(my_file,  to_int=False).read()


print("lxml_parse :")
count=0
start = time.time()
for i in lxml_parse(my_file, depth=2, compression=my_compression, object_processor=ip ):
    count+=1
    #print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

print("lxml_iterparse :")
count=0
start = time.time()
for i in lxml_iterparse(my_file, depth=2, compression=my_compression, object_processor=ip):
    count+=1
    # print("RETOUR")
    #print(i)
    # print("\n")
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

count=0
print("xmltodict :")
start = time.time()
for i in xmltodict(compression=my_compression):
    count+=1
    # print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

count=0
print("xml_parse :")
start = time.time()
for i in xml_parse(my_file, depth=2, compression=my_compression):
    count+=1
    # print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

count = 0
print("xml_iterparse :")
start = time.time()
for i in xml_iterparse(my_file, depth=2, compression=my_compression):
    count += 1
    # print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")
