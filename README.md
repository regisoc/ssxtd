# semi structured xml to dict

ssxtd is an xmlreader similar to xmltodict, but supporting semi structured xml, and providing a more flexible environnment.
ssxtd use either of :
  * the lxml package
  * the native package ElementTree
  * the defusedxml package 
  
Globally, lxml is performing better than ElementTree

## Getting started

  * if you can't install lxml, and are limitted in RAM, use :
  `parsers.xml_iterparse(my_file)`
  
  * if you can't install lxml, and are NOT limitted in RAM, use :
  `parsers.xml_parse(my_file)`
  
  * if you CAN install lxml, and are limitted in RAM, use :
  `parsers.lxml_iterparse(my_file)`
  
  * if you CAN install lxml, and are NOT limitted in RAM, use :
  `parsers.lxml_parse(my_file)`
  
depth is the depth of the tag you want to parse

## Mixed tag and text 

ssxtd will automatically convert mixed tags and text to a string, keeping the same order as in the xml.

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

note : atm, in a zip compression mode, only .xml situated at the root of the zip will be read

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

## Secure

you can use :
  `parsers.dxml_iterparse(my_file)`
or
  `parsers.dxml_parse(my_file)`

to use the defusedxml.ElementTree instead of xml.etree.ElementTree

## Run tests

in the root directory, run :
`pytest`

for running a single file, you can do :
`python -c "import ssxtd.tests.test_malformed_xml"`

## Performances of the parsing functions

  lxml_parse :
  17.63099956512451 seconds
  7764 processed values


  lxml_iterparse :
  19.163238525390625 seconds
  7764 processed values


  xml_parse :
  17.3682701587677 seconds
  7764 processed values


  xml_iterparse :
  27.15250539779663 seconds
  7764 processed values


  xmltodict (other lib) :
  18.277526140213013 seconds
  7764 processed values


