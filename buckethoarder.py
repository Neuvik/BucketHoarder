#!/usr/bin/python3
import argparse
from ast import arguments # This is to properly parse arguments and use them as sets.
from distutils import filelist 
import os
import sys
import json
import requests
import pyjq
import concurrent.futures
from urllib.parse import urlparse
from dotenv import load_dotenv


verbose = False

#process arguments
def arguments():
    parser = argparse.ArgumentParser(description='Download files from anonymous buckets that are indexed by Grayhat Warfare')
    parser.add_argument("-a", "--api-key", action='store', help="Your personal api key for Grayhat Warfare", required=False, default="")
    parser.add_argument("-f", "--function", action='store', help="Values as follow, p to print file listing with bucket id, name and url, d to download all files returned via query, b to search by bucket names. Default is download files", required=True, default="f")
    parser.add_argument("-t", "--search-term", action='store', help="Terms to search for in path or filename", nargs='*')
    parser.add_argument("-i", "--include-ext", action='store', help="File extensions to include in search", nargs='*')
    parser.add_argument("-e", "--exclude-ext", action='store', help="File extensions to exclude in search", nargs='*')
    parser.add_argument("-p","--full-path", action='store', help="Set to 1 to search full file path, set to 0 to just search file name", type=str, default="0")
    parser.add_argument("-d","--directory", action='store', help="Direcory to store downloaded files",  default="downloads")
    parser.add_argument("-v","--verbose", action='store_true', default=False)
    return parser.parse_args()

#get count of total number of files
def item_count(api_key,search_terms,include_ext,exclude_ext,full_path,verbose):
    url="https://buckets.grayhatwarfare.com/api/v2/files"
    if search_terms:
        url+='?keywords='+search_terms
    if include_ext:
        url+="&extensions="+include_ext
    if exclude_ext:
        url+="&stopextensions="+exclude_ext 
    if full_path:
        url+="&full-path="+full_path
    if api_key:
        headers={"Authorization": "Bearer "+api_key}
    r = requests.get(url, headers=headers)
    if verbose == True:
        print("[*]    For Debugging Purpses the URL Query is: " +str(r.url)) # Comment out in debug OR redact and log.
    items = pyjq.all('.meta.results', json.loads(r.text))[0]
    print("[*]    Total Number of items: "+str(items))
    return(items)

#Return all file urls as a list
def get_file_list(api_key,search_terms,include_ext,exclude_ext,full_path):
    file_list=[]
    url="https://buckets.grayhatwarfare.com/api/v2/files"
    if search_terms:
        url+='?keywords='+search_terms
    if include_ext:
        url+="&extensions="+include_ext
    if exclude_ext:
        url+="&stopextensions="+exclude_ext 
    if full_path:
        url+="&full-path="+full_path
    if api_key:
        headers={"Authorization": "Bearer "+api_key}
    r = requests.get(url, headers=headers)
    if verbose == True:
        print("API Request: "+r.url)
    #print(r.text)
    file_list = pyjq.all('.files[] .url', json.loads(r.text))
    #file_list.extend(pagination_file_list)
        #print(pagination_file_list)
    if verbose == True:
        print(file_list)
    return(file_list)

#Iterate through API pagination and return all bucket ids, bucket names and urls
def print_file_list(api_key,search_terms,include_ext,exclude_ext,full_path,verbose):
    file_list=[]
    url="https://buckets.grayhatwarfare.com/api/v2/files"
    if search_terms:
        url+='?keywords='+search_terms
    if include_ext:
        url+="&extensions="+include_ext
    if exclude_ext:
        url+="&stopextensions="+exclude_ext 
    if full_path:
        url+="&full-path="+full_path
    if api_key:
        headers={"Authorization": "Bearer "+api_key}
    r = requests.get(url, headers=headers)
    if verbose == True:
        print("API Request: "+r.url)
    #print(r.text)
    file_list = pyjq.all('.files[] .url', json.loads(r.text))
    #file_list.extend(pagination_file_list)
        #print(pagination_file_list)
    if verbose == True:
        print(file_list)
    return(file_list)

#for link in file_list:
def download_file(file_url,directory):
    url = urlparse(file_url)
    if verbose == True:
        print("URL is: "+url.scheme+url.netloc+url.path)
        print("Directory is: "+directory)
    fullname=os.path.join(directory,(url.netloc+url.path))
    name=os.path.basename(url.path)
    exist = os.path.isdir(os.path.dirname(fullname))
    if not exist:
        try:
            os.makedirs(os.path.dirname(fullname))
        except Exception as inst:
            pass

    filename = name
    if verbose == True:
        print("Filename is: "+fullname)

    if not os.path.isfile(fullname):
        print('Downloading: ' + file_url)
        try:
            r = requests.get(file_url, stream = True)
            with open(fullname, 'wb') as f:
                for ch in r:
                    f.write(ch)
                f.close()
        except Exception as inst:
            print(inst)
            print('  Encountered unknown error. Continuing.')

#def download_files(args):
def download_files(api_key,search_terms,include_ext,exclude_ext,full_path,output_directory,verbose):

    total_results=item_count(api_key,search_terms,include_ext,exclude_ext,full_path,verbose)

    print("Total files: "+str(total_results))

    file_list=get_file_list(api_key,search_terms,include_ext,exclude_ext,full_path)
    
    print("Total number of files: "+str(len(file_list)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for url in file_list:
            futures.append(executor.submit(download_file, file_url=url, directory=output_directory))
        for future in concurrent.futures.as_completed(futures):
            a=future.result()


def print_files(args):
    print(args)

def search_buckets(args):
    if args.verbose == True:
        print(args)

def main():
    load_dotenv()
    args = arguments()

    include_ext=""
    exclude_ext=""
    search_terms="!"

    verbose = args.verbose    
    if args.verbose:
        verbose = args.verbose
    if args.search_term:
        search_terms= '%20'.join([str(elem) for elem in args.search_term])
        if verbose == True:
            print (search_terms)
    if args.include_ext:
        include_ext= ','.join([str(elem) for elem in args.include_ext])
        if verbose == True:
            print (include_ext)
    if args.exclude_ext:
        exclude_ext= ','.join([str(elem) for elem in args.exclude_ext])
        if verbose == True:
            print (exclude_ext)
    if args.full_path:
        full_path=str(args.full_path)
        if verbose == True:
            print (full_path)
    if args.directory:
        output_directory=args.directory
        print ("Saving files to "+output_directory)
    if (os.getenv("API_KEY")):
        api_key=os.getenv("API_KEY")
        if verbose == True:
            print (api_key)
    if not (os.getenv("API_KEY")):
        api_key=args.api_key
        if verbose == True:
            print (api_key)
    if api_key == "":
        print("Please set the API Key in the .env file, or use the -a flag")

    if args.verbose == True:
        print(f'''
The following are arguments passed in: 

        [*]     API_KEY:        *****
        [*]     FUNCTION:       {args.function}
        [*]     SEARCH_TERM:    {args.search_term}
        [*]     INCLUDE_EXT:    {args.include_ext}
        [*]     EXCLUDE_EXT:    {args.exclude_ext}
        [*]     FULL_PATH:      {args.full_path}
        [*]     DIRECTORY:      {args.directory}
        [*]     VERBOSE:        {args.verbose}
        ''')

    match args.function:
        case "p":
            total_results=item_count(api_key,search_terms,include_ext,exclude_ext,full_path,verbose)
            print_file_list(api_key,search_terms,include_ext,exclude_ext,full_path,verbose)
        case "d":
            download_files(api_key,search_terms,include_ext,exclude_ext,full_path,output_directory,verbose)
        case "b":
            search_buckets
        case _:
            print("Invalid value for function")
    

if __name__ == "__main__":
    print(f'''
+-----------------------------------------------------------------------------+
:    ______            _        _   _   _                     _               ;
:    | ___ \          | |      | | | | | |                   | |              ;
:    | |_/ /_   _  ___| | _____| |_| |_| | ___   __ _ _ __ __| | ___ _ __     ;
:    | ___ \ | | |/ __| |/ / _ \ __|  _  |/ _ \ / _` | '__/ _` |/ _ \ '__|    ;
:    | |_/ / |_| | (__|   <  __/ |_| | | | (_) | (_| | | | (_| |  __/ |       ;
:    \____/ \__,_|\___|_|\_\___|\__\_| |_/\___/ \__,_|_|  \__,_|\___|_|       ;
:                                                                             ;
:                                                                             ; 
:                                                                       cd /      ;
:   Neuvik's BucketHoarder for use with the grayhatwarfare API.               ;
:                                                                             ;
`-----------------------------------------------------------------------------+


    ''')
    main()
