# semi structured xml to dict

ssxtd is an xmlreader similar to xmltodict, but supporting semi structured xml, and providing a more flexible environnment.
ssxtd use either of :
  * the native xml package
  * the lxml package
  * the defusedxml package 
  
Globally, stick to native xml package. It's the faster for most situations.

Note : ssxtd was created to parse very big files, as a result, the default parsing depth is 2 and the parsing functions are generators. 

## Quickstart

  ```
  pip install ssxtd
  ```
  ```
  from ssxtd import parsers
  result = next(parsers.xml_parse(my_file, depth=0))
  ```



## What if ...



### ...i want to parse big files?

use :  
`parsers.xml_iterparse(my_file)`  

note : by default, it will return depth 2 elements.  
  


### ...my xml file has mixed tag and text?

ssxtd will automatically convert mixed tags and text to a string, keeping the right order.
  


### ...i want to use defusedxml to secure my app?

use :  
`parsers.dxml_parse(my_file)`  
or  
`parsers.dxml_iterparse(my_file)`  
  


### ...i want to use lxml?

use :  
`parsers.lxml_parse(my_file)`  
or  
`parsers.lxml_iterparse(my_file)`  

note : it will be slower than xml_parse and xml_iterparse
  



## Options

### depth

you can adjust the depth level of the returned objects, even when not using iterparse.

note : you can't use depth = 0 when using iterparse

### trim_spaces

will trim spaces for each value found. can be usefull when you have some ugly xml like:
```
<root>
  <text>we have
  some indentation
  problems
  </text>
</root>
```

### del_empty (default to True)

if set to False, will not remove empty tags

### cleanup_namespaces

if set to False, will not remove namespaces

### verbose

if set to True, will show a progression bar \o/

### recover

if set to True, will recover from malformed xml ( cf test_malformed_xml.py)

note : lxml_parse and lxml_iterparse will use the lxml abilities whereas the others will use a BeautifulSoup transformation

### compression

ssxtd can manage ZIP, GZIP, ByteIO, and path to files

for ZIP and GZIP, you must set the parameter "compression" to either "gz" or "zip"
```
parsers.xml_parse(my_file, compression="gz"):
```
you can also set the parameter to "auto", ssxtd will then auto detect the file type from the extension (.xml, .zip, or .gz)

note : atm, in a zip compression mode, only .xml files situated at the root of the zip file will be read

### object_processorr

if you specify the parameter "object_processor=my_function" when calling a parser, your function will be called for each object 

```
see bin/run_exemple.py
```
        

Allows to do special actions like merging tags directly during the parsing

### value_processor

if you specify the parameter "value_processor=my_function" when calling a parser, your function will be called for each value found 

e.g a simple type conversion :
```
def try_conversion(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            pass
        try:
            return float(value)
        except (ValueError, TypeError):
            pass
        return value
```        



## Requirements

### Python

python >= v3.7.0b1  
due to https://github.com/python/cpython/commit/066df4fd454d6ff9be66e80b2a65995b10af174f  
you CAN use older version of pythons ( i tested up to 3.5) but you won't be able to read zip files  

### Libs

- bs4
- tqdm

## Run tests

install pytest:  
`pip install pytest`  
in the root directory, run :  
`pytest`  
for running a single file, place yourself at the root folder and run :  
`python -c "import ssxtd.tests.test_malformed_xml"`  

## Performances of the parsing functions

time to parse https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n0001.xml.gz  
GZ file size : 19MB  
extracted size : 185MB  
proc : i7-7700HQ  

| Function  | XML file | GZ file | ZIP file (no compression)|
| ------------- | ------------- | ------------- | ------------- |
|xml_parse|32.76501545000065|36.07715339999959|33.419777400000385|
|xml_iterparse|37.56028480000168|42.16279835000023|39.137448499999664|
|lxml_parse|37.464776250000796|38.880011499999455|37.046347550000064|
|lxml_iterparse|47.04024449999997|45.959421049999946|45.05521540000154|
|dxml_parse|41.52063830000043|40.07632935000038|38.88691465000011|
|dxml_iterparse|45.195273199999065|44.895784000000276|44.13825424999959|

for much more details please see ssxtd\benchmarks\results\result.csv
