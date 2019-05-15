import urllib.request
import glob
from .. import parsers
import timeit
import gzip
import zipfile
import shutil


gz_filepath = "/tmp/lucan_test.xml.gz"
xml_filepath = "/tmp/lucan_test.xml"
zip_filepath = "/tmp/lucan_test.zip"

functions = [parsers.xml_iterparse, parsers.xml_parse, parsers.lxml_parse, parsers.lxml_iterparse, parsers.dxml_parse, parsers.dxml_iterparse]

def gen_data(filepath, function):
    count = 0
    for _ in function(filepath, depth=2, compression="gz", value_processor=None, object_processor=None):
        count += 1
        pass
    print(str(count) + " values processed")


def dl_files():
    url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n0001.xml.gz"
    with urllib.request.urlopen(url) as response, open(gz_filepath, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def gz_extract():
    with gzip.open(gz_filepath, 'rb') as f_in:
        with open(xml_filepath, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def do_the_zip():
    z = zipfile.ZipFile(zip_filepath, "w")
    z.write(xml_filepath)
    z.close

def do_setup():
    print("setuping the setup")
    dl_files()
    # gz_extract()
    # do_the_zip()
    print("setuping finished")

# file_list = glob.glob("/tmp/lucan/xsp/data/*")
# lf = len(file_list)



while True:
    try:
        
     

        for n, f in enumerate(functions):
            print("benchmarking " + f.__name__ + " for " + gz_filepath)
            t = timeit.timeit('gen_data(gz_filepath, parsers.'+f.__name__+')', 'from ssxtd.benchmarks.run import gen_data, gz_filepath, functions; from ssxtd import parsers', number=5)
            print(t)
        break
    except Exception as e:
        pass
        #print("error" + str(e))
        raise Exception (e)
        break
        #do_setup()

        

