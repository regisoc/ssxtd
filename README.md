# semi structured xml to dict

ssxtd is an xmlreader similar to xmltodict, but supporting semi structured xml, and providing a more flexible environnment.

## Getting started

WIP

## Mixed tag and text 

ssxtd will convert mixed tags and text to a string, keeping the order of the xml.

## Flexible

### Object processor

Allows to do special actions like merging tags (see bin/run_exemple.py ) directly during the parsing

### Value processor

Allows to do special actions like conversions (see the default value processor in ssxtd/parsers.py ) (Soon visible, WIP)

## Performances 

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


xmltodict :
18.277526140213013
7764 processed values


