#!/usr/bin/env python

# Import all the required packages
import os
import sys
import wikixmlparser
import wikindexer

def main():
    # Environment and global variables
    if len(sys.argv) != 3:
        print("[ERROR] Insufficient input parameters\n")
        sys.exit()

    s_xml_dump_file = sys.argv[1]
    s_index_path = sys.argv[2]
    if s_index_path[-1] != '/':
        s_index_path + '/'
    s_data_path = os.getcwd()+"/data/"

    # create data and index directories (mkdir -p)
    if not os.path.exists(s_index_path): os.makedirs(s_index_path)
    if not os.path.exists(s_data_path): os.makedirs(s_data_path)

    o_wiki_parser = wikixmlparser.WikiXmlParser(s_xml_dump_file, s_data_path)
    d_bow = o_wiki_parser.extractXmlData()
    print ("[INFO] XML Parsing Completed")

    o_wiki_indexer = wikindexer.WikiIndexer(s_index_path)
    o_wiki_indexer.run(d_bow)
    print ("[INFO] Index Creation Completed")

# Script starts here - Main
if __name__ == '__main__':
    main()
