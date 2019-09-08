#!/usr/bin/env python

# Import all the required packages
import os
import sys
import wikisearch

# write query results to a file
def outputResults(data_files_path_parm,
                  d_relevant_docs,
                  s_query_results_file_parm):
    with open(s_query_results_file_parm, "w+") as f_results:
        for s_key in d_relevant_docs:
            l_doc_ids = d_relevant_docs[s_key]
            for s_doc_id in l_doc_ids:
                s_block_id = s_doc_id.split(".")[0]
                s_data_file = data_files_path_parm +"/"+s_block_id+"/"+s_doc_id
                with open(s_data_file, "r") as f_data:
                    s_title_name = f_data.readline()
                    f_results.write(s_title_name)
            f_results.write("\n")

def main():
    # read the search string from input
    if len(sys.argv) != 4:
        print("[ERROR] Missing/Invalid input parameters for search")
        print("USAGE: python InitSearch.py path_to_index path_to_query_file path_to_result_file")
        sys.exit()

    s_data_files_path      = os.getcwd()+'/data/'
    s_index_path           = sys.argv[1]
    if s_index_path[-1] != '/':
        s_index_path = s_index_path + '/'
    s_search_queries_file  = sys.argv[2]
    s_search_results_file  = sys.argv[3]

    o_wiki_search = wikisearch.WSE(s_index_path,
                                   s_data_files_path,
                                   s_search_queries_file)
    d_relevant_files = o_wiki_search.run()
    #print(d_relevant_files)

    outputResults(s_data_files_path,
                  d_relevant_files,
                  s_search_results_file)

if __name__ == '__main__':
    main()