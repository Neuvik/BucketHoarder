#!/usr/bin/python3
import magic
import os
import argparse

#process arguments
def arguments():
    parser = argparse.ArgumentParser(description='This will classify and identify files for you')
    parser.add_argument("-d","--directory", action='store', help="Direcory to store downloaded files",  default="downloads", required=True)
    return parser.parse_args()

def main():
    args = arguments()

    if args.directory:
        directory=args.directory
        print (directory)
    if not args.directory:
        print("Please specify a directory to classify")
        exit()

    interesting_file = directory+"/interesting_files.txt"
    uninteresting_categories = ["data", "empty"]

    file = open(interesting_file, 'w')

    for root,dir,files in os.walk(directory, topdown = False):    
        for name in files:
            full_path = os.path.join(root,name)
            what_file_type = magic.from_file(os.path.join(root,name))
            print('File: {}, File Type: {}'.format(full_path,what_file_type))
            if not any(x in what_file_type for x in uninteresting_categories):
                file.write('File: {}, File Type: {}\r\n'.format(full_path,what_file_type))
            
    file.close()
#  + os.path.join(root,name)) + ", File Type: " magic.from_file(os.path.join(root,name))

if __name__ == "__main__":
    print(f'''
+-----------------------------------------------------------------------------+
: files.py                                                                    ;
:                                                                             ;
:   This is for use with BucketHoarder to Classify all files in a directory.  ;
:                                                                             ;
`-----------------------------------------------------------------------------+


    ''')
    main()