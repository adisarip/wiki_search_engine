#!/usr/bin/env python

# Import all the required packages
import os
import sys
import wikixmlparser
import wikindexer
import multiprocessing as mp

gn_max_doc_count = 10000 # maximum docs under each block

def worker(q_data_blocks_parm,
           n_blocks_parm,
           n_last_block_count_parm):
    while not q_data_blocks_parm.empty():
        try:
            n_block = q_data_blocks_parm.get(False)
            print("[INFO] "+mp.current_process().name+":Processing Block:", n_block)
            o_wiki_indexer = wikindexer.WikiIndexer(s_index_path,
                                                    s_data_path)
            if (n_block == n_blocks_parm):
                n_docs = n_last_block_count_parm
            else:
                n_docs = gn_max_doc_count
            
            o_wiki_indexer.run(n_block, n_docs)
        except Exception as exp:
            print("Execption in Process:", mp.current_process().name)
            print(exp)
            pass

def main(d_penv_parm):

    s_xml_dump_file = d_penv["xml_dump_file"]
    s_index_path    = d_penv["index_path"]
    s_data_path     = d_penv["data_path"]

    o_wiki_parser = wikixmlparser.WikiXmlParser(s_xml_dump_file,
                                                s_data_path)
    o_wiki_parser.extractXmlData()
    print ("[INFO] XML Parsing Completed")

    # Get data blocks info
    with open(s_data_path+"/block.data", "r") as f_block_data:
        s_last_block, s_last_block_count = f_block_data.readline().split(",")
    n_blocks = int(s_last_block)
    n_last_block_count = int(s_last_block_count)

    # Forking multiple processes to process the data blocks
    q_data_blocks = mp.Queue()
    [q_data_blocks.put(x) for x in range(1, n_blocks+1)]

    n_processes = 10
    l_processes = [mp.Process(target=worker,
                              args=(q_data_blocks, n_blocks, n_last_block_count))
                              for x in range(n_processes)]
    for p in l_processes:
        p.start()

    for p in l_processes:
        p.join()
    
    print ("[INFO] Index Creation Completed")


# Script starts here - Main
if __name__ == '__main__':
    # Environment and global variables
    if len(sys.argv) != 3:
        print("[ERROR] Insufficient input parameters\n")
        sys.exit()

    s_xml_dump_file = sys.argv[1]
    s_index_path = sys.argv[2]
    if s_index_path[-1] != '/':
        s_index_path = s_index_path + '/'
    s_data_path = os.getcwd()+"/wikidata/"

    # create required directories (mkdir -p)
    if not os.path.exists(s_index_path): os.makedirs(s_index_path)
    if not os.path.exists(s_data_path): os.makedirs(s_data_path)

    d_penv = dict()
    d_penv["xml_dump_file"] = s_xml_dump_file
    d_penv["index_path"]    = s_index_path
    d_penv["data_path"]     = s_data_path

    main(d_penv)


