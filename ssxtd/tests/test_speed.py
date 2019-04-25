import gzip
import zlib
import io
from ssxtd import parsers

import time

my_file = "exemple.xml"
my_compression = None

print("lxml_parse :")
count = 0
start = time.time()
for i in parsers.lxml_parse(my_file, depth=2, compression=my_compression):
    count += 1
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

print("lxml_iterparse :")
count = 0
start = time.time()
for i in parsers.lxml_iterparse(my_file, depth=2, compression=my_compression):
    count += 1
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

count = 0
print("xml_parse :")
start = time.time()
for i in parsers.xml_parse(my_file, depth=2, compression=my_compression):
    count += 1
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

count = 0
print("xml_iterparse :")
start = time.time()
for i in parsers.xml_iterparse(my_file, depth=2, compression=my_compression):
    count += 1
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

""" # with xmltodict
count=0
print("xmltodict stremming mode :")
start = time.time()
for i in xmltodict(compression=my_compression):
    count+=1
    # print(i)
end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")

# with xmltodict
count=0
print("xmltodict streamming mode :")
start = time.time()

xmltodict.parse(my_file)


end = time.time()
print(end - start)
print(str(count) + " entrées traitées\n\n")
     """
