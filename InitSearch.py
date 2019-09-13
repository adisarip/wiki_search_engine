#!/usr/bin/env python

# Import all the required packages
import os
import sys
import wikisearch
from datetime import datetime

# write query results to a file
def getTitleNames(data_files_path_parm,
                  d_relevant_docs):
    l_title_names = []
    for s_key in d_relevant_docs:
        l_doc_ids = d_relevant_docs[s_key]
        for s_doc_id in l_doc_ids:
            s_block_id = s_doc_id.split(".")[0]
            s_data_file = data_files_path_parm +"/"+s_block_id+"/"+s_doc_id
            with open(s_data_file, "r") as f_data:
                l_title_names.append(f_data.readline().rstrip())
    return l_title_names

def main():
    # read the search string from input
    if len(sys.argv) != 2:
        print("[ERROR] Missing/Invalid input parameters for search")
        print("USAGE: python InitSearch.py <path_to_index>")
        sys.exit()

    s_data_files_path      = os.getcwd()+'/wikidata/'
    s_index_path           = sys.argv[1]
    if s_index_path[-1] != '/':
        s_index_path = s_index_path + '/'
    
    o_wiki_search = wikisearch.WSE(s_index_path,
                                   s_data_files_path)
    while (True):
        try:
            s_search_query  = input("[0 or 'q' to exit] Enter Search Query: ")
            if (s_search_query == "0" or s_search_query == "q"):
                break
            if (s_search_query == ""):
                continue
            tstart = datetime.now()
            d_relevant_files = o_wiki_search.run(s_search_query)
            tend = datetime.now()

            l_search_results = getTitleNames(s_data_files_path,
                                            d_relevant_files)
        except:
            if (len(s_search_query) < 3):
                print("[INFO] Query size too small. Enter minimum 3 characters to search")
            else:
                print("[WARN] Invalid search query. Input should be alphanumeric")
            continue
        
        print("\n=== Top 10 results ===")
        for result in l_search_results:
            print(result)
        print("===================================")
        print ("Search Time: {} seconds".format(tend - tstart))
        print("===================================\n")


if __name__ == '__main__':
    main()