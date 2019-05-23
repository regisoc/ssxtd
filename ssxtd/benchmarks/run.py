import urllib.request
import glob
from .. import parsers
import timeit
import gzip
import zipfile
import shutil
import os
import csv
import xml.etree.ElementTree as ET
import time
import resource
import sys
import gc
import traceback
from datetime import datetime

result_dir = "./ssxtd/benchmarks/results/"
working_dir = "/tmp/"
url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n0001.xml.gz"
gz_filename = "ssxtd_test.xml.gz"
xml_filename = "ssxtd_test.xml"
zip_filename = "ssxtd_test.zip"
gz_filepath = working_dir + gz_filename
xml_filepath = working_dir + xml_filename
zip_filepath = working_dir + zip_filename
tag = "PubmedArticle"
start_tag = "<PubmedArticleSet>"
end_tag = "</PubmedArticleSet>"
filetype_modes = ["xml", "gz", "zip"]
#sizes = [10, 100, 250,500,750,1000]
sizes = [10,100]
#sizes = [10]
#modes = filetype_modes + sizes

soft_limit = 0 
mem_ratio = 0.7
functions = [parsers.xml_parse, parsers.xml_iterparse, parsers.lxml_parse, parsers.lxml_iterparse, parsers.dxml_parse, parsers.dxml_iterparse]

# modes var will determine what type of benchmark to run:
# filetype_mode or sizes, or both!

# modes = filetype_modes
# modes = filetype_modes + sizes
modes = sizes



def memory_limit():
    """if we don't limit the memory used, the program will be killed
    """
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    soft_limit = get_memory() * mem_ratio
    print("setting soft mem limit to " + str(soft_limit) + " Bytes")
    resource.setrlimit(resource.RLIMIT_AS, (soft_limit , hard))

def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory * 1024
    
def gen_data(filepath, function):
    count = 0
    for _ in function(filepath, depth=2, compression="auto", value_processor=None, object_processor=None):
        count += 1
        pass
    print(str(count) + " values processed")


def dl_files():
    
    with urllib.request.urlopen(url) as response, open(gz_filepath, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def gz_extract():
    """from a gz file extract the xml
    """
    with gzip.open(gz_filepath, 'rb') as f_in:
        with open(xml_filepath, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def do_the_zip():
    """from xml to zip transformation
    """
    z = zipfile.ZipFile(zip_filepath, "w")
    z.write(xml_filepath)
    z.close

def do_setup():
    """dl/create files for the benchmark
    """
    print("setuping the setup\nwaiting 5s before starting")
    time.sleep(5)
    dl_files()
    gz_extract()
    do_the_zip()
    xml_generation()
    print("setuping finished")

def xml_generation():
    """generate all xml needed for the sizes mode
    """
    
    for max_size in sizes:
        byte_file = open(xml_filepath, "rb")
        filename = working_dir + "ssxtd_test_" + str(max_size) +".xml"
        with open(filename, 'wb') as new_file:
            #new_file.write(b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            new_file.write(start_tag.encode())
            max_size_reached = False
            while max_size_reached ==False:
                byte_file.seek(0)
                for _, elem in ET.iterparse(byte_file, events=('end', )):
                    if elem.tag == tag:
                        new_file.write(ET.tostring(elem))

                        #size = os.path.getsize(new_file)
                        size = new_file.tell()
                        mb_size = size/(1024.0*1024.0)
                        if mb_size > max_size:
                            new_file.write(end_tag.encode())
                            max_size_reached = True
                            break
        print("finished writing "+ str(max_size) + "MB test file")
        

def start():
    memory_limit()

    

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    
    prompt = " [y/N] "
    question = "Do you want to download/generate the test files? (default : no)"

    while True:
        print(question + prompt)
        choice = input().lower()
        if choice == '' :
            answer = valid["no"]
            break
        elif choice in valid:
            answer = valid[choice]
            break
        else:
            print("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

    if answer:
        do_setup()


    error_count = 0
    number = 2

    table = [["" for x in range(len(modes)+1)] for y in range(len(functions)+1)] 
    table[0][0]="parsing_function\\parsed_file"
    for n, f in enumerate(functions):
        table[n+1][0]=f.__name__


    while True:
        try:
            
            for no_mode, m in enumerate(modes):
                
                if m =="gz":
                    my_file = gz_filepath
                elif m =="xml":
                    my_file = gz_filepath
                elif m =="zip":
                    my_file = gz_filepath
                # size mode
                else:
                    my_file = working_dir + "lucan_test_" + str(m) +".xml"
                    m = str(m)+"MB_xml"

                table[0][no_mode+1] = m


                for no_func, f in enumerate(functions):
                    print("benchmarking " + f.__name__ + " for " + my_file)
                    try:
                        t = timeit.timeit('run.gen_data("'+my_file+'", parsers.'+f.__name__+')', 'import ssxtd.benchmarks.run as run; from ssxtd import parsers', number=number)
                        real_time = t/number
                        print(real_time)
                        table[no_func+1][no_mode+1]=real_time
                    except MemoryError:
                        sys.stderr.write('\n\nERROR: Memory Exception\n')
                        table[no_func+1][no_mode+1]="Memory Exception"
                    except Exception as e:
                        print(traceback.format_exc())
                        
                    print("\n")
                    gc.collect()

                print("\n\n")

            with open(result_dir+"result.csv","a") as my_csv:
                

                date = datetime.today().strftime('%Y-%m-%d')
                my_csv.write("SSXTD BENCHMARK\n")
                my_csv.write("start date : " +date+ "\n")
                my_csv.write("maximum allocated memory (RAM + SWAP) : " + str(get_memory() * mem_ratio /(10 ** 9)) + "GB\n")
                my_csv.write("CPU : \n")
                my_csv.write("ssxtd version : 1.0.8\n\n")
                csvWriter = csv.writer(my_csv,delimiter=',')
                csvWriter.writerows(table)
                my_csv.write("\n\n\n\n")
            break
        except Exception as e:
            error_count +=1
            #raise Exception (e)
            if error_count > 2:
                print("aborting test")
                raise e
            print("error" + str(e))
            print("gonna get the files again")
            do_setup()

            

