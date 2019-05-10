import glob
import json
import parsers

def gen_data( to_int=False):
        filepath = "/tmp/lucan/xavier_pub_hmdb_metabolite/data/hmdb_metabolites.zip"

        
        yield from parsers.lxml_iterparse(filepath, depth=2, compression="zip", value_processor=None, object_processor=None)



for i in gen_data():
    j = json.dumps(i)
    print(j)
    break

        
