import glob
import json
import parsers

def gen_data( to_int=False):
        file_list = glob.glob("/tmp/lucan/xsp/data/*.gz")
        lf = len(file_list)
        print("\nExtracting records from files\n")
        
        for i, filepath in enumerate(file_list):
            print('[{}/{}] Reading: {}'.format(i + 1, lf, filepath))
            #yield from parsers.xml_iterparse(filepath, depth=2, compression="gz", value_processor=None, object_processor=None)
            yield from parsers.xml_parse(filepath, depth=2, compression="gz", value_processor=None, object_processor=None, verbose=True)



for i in gen_data():
    pass

        
