# semi structured xml to dict

ssxtd is an xmlreader similar to xmltodict, but supporting semi structured xml, and providing a more flexible environnment.
ssxtd use either of :
  * the lxml package
  * the native package ElementTree
  
the choice, and installation, in up to the user.
Globally, lxml is performing better than ElementTree

## Getting started

  * if you can't install lxml, and are limitted in RAM, use :
  `parsers.xml_iterparse(my_file, depth=2)`
  
  * if you can't install lxml, and are NOT limitted in RAM, use :
  `parsers.xml_parse(my_file, depth=2)`
  
  * if you CAN install lxml, and are limitted in RAM, use :
  `parsers.lxml_iterparse(my_file, depth=2)`
  
  * if you CAN install lxml, and are NOT limitted in RAM, use :
  `parsers.lxml_parse(my_file, depth=2)`
  
depth is the depth of the tag you want to parse

## Mixed tag and text 

ssxtd will convert mixed tags and text to a string, keeping the order of the xml.

## Flexible

### Compressed files
if you specify the parameter "compression" when calling a parser, the file will be decompressed
accepted values : "gz", "zip"
```
parsers.xml_parse(my_file, depth=2, compression="gz"):
```

### Object processor

if you specify the parameter "object_processor=my_function" when calling a parser, your function will be called for each object 

```
WIP (see bin/run_exemple.py ) 
```
        

Allows to do special actions like merging tags directly during the parsing

### Value processor

if you specify the parameter "object_processor=my_function" when calling a parser, your function will be called for each object 

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
## Performances of the parsing functions

lxml_parse :
17.63099956512451
7764 processed values


lxml_iterparse :
19.163238525390625
7764 processed values


xml_parse :
17.3682701587677
7764 processed values


xml_iterparse :
27.15250539779663
7764 processed values


xmltodict (other lib) :
18.277526140213013
7764 processed values


