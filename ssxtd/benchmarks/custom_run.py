import urllib.request
import glob
from .. import parsers
import timeit
import gzip
import zipfile
import shutil
import os
import csv


def gen_data(filepath, function):
    count = 0
    for _ in function(filepath, depth=2, compression="auto", value_processor=None, object_processor=None):
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
    gz_extract()
    do_the_zip()
    print("setuping finished")

# file_list = glob.glob("/tmp/lucan/xsp/data/*")
# lf = len(file_list)

gz_filepath = "/tmp/lucan_test.xml.gz"
xml_filepath = "/tmp/lucan_test.xml"
zip_filepath = "/tmp/lucan_test.zip"

functions = [parsers.xml_iterparse, parsers.xml_parse, parsers.lxml_parse, parsers.lxml_iterparse, parsers.dxml_parse, parsers.dxml_iterparse]
modes = ["xml", "gz", "zip"]

if not os.path.isfile(gz_filepath) or not os.path.isfile(xml_filepath) or not os.path.isfile(zip_filepath):
    do_setup()

error_count = 0
number = 5

table = [["" for x in range(len(modes)+1)] for y in range(len(functions)+1)] 

for n, f in enumerate(functions):
    table[n+1][0]=f.__name__


while True:
    try:
        
        for no_mode, m in enumerate(modes):
            table[0][no_mode+1] = m
            if m =="gz":
                my_file = gz_filepath
            elif m =="xml":
                my_file = xml_filepath
            elif m =="zip":
                my_file = zip_filepath


            for no_func, f in enumerate(functions):
                print("benchmarking " + f.__name__ + " for " + my_file)
                t = timeit.timeit('gen_data("'+my_file+'", parsers.'+f.__name__+')', 'from ssxtd.benchmarks.run import gen_data; from ssxtd import parsers', number=number)
                real_time = t/number
                print(real_time)
                table[no_func+1][no_mode+1]=real_time
                print("\n")

            print("\n\n")

        with open("result.csv","w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(table)
        break
    except Exception as e:
        error_count +=1
        #raise Exception (e)
        if error_count > 5:
            raise e
        print("error" + str(e))
        print("gonna get the files again")
        do_setup()

        

