from xml_file_reader import XMLFileReader

#from collections import defaultdict
from parsers import *

import time
my_file = "exemple.xml"



def xmltodict():
    yield from XMLFileReader(my_file,  to_int=False).read()


print("lxml_parse :")
count=0
start = time.time()
for i in lxml_parse(my_file, depth=2 ):
    count+=1
    print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

print("lxml_iterparse :")
count=0
start = time.time()
for i in lxml_iterparse(my_file, depth=2):
    count+=1
    # print("RETOUR")
    print(i)
    # print("\n")
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

count=0
print("xmltodict :")
start = time.time()
for i in xmltodict():
    count+=1
    print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

count=0
print("xml_parse :")
start = time.time()
for i in xml_parse(my_file, depth=2):
    count+=1
    print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

count = 0
print("xml_iterparse :")
start = time.time()
for i in xml_iterparse(my_file, depth=2):
    count += 1
    print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")
