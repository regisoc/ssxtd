import glob
import json
from .. import parsers

def gen_data( to_int=False):
        file_list = glob.glob("/tmp/lucan/xsp/data/*.gz")
        lf = len(file_list)
        print("\nExtracting records from files\n")
        
        for i, filepath in enumerate(file_list[834:]):
            print('[{}/{}] Reading: {}'.format(i + 1, lf, filepath))
            yield from parsers.lxml_parse(filepath, depth=2, compression="gz", value_processor=None, object_processor=None)



for i in gen_data():
    j = json.dumps(i)
    if "http://www.w3.org/1998/Math/MathML" in j:
        print(i["MedlineCitation"]["PMID"])

        
