#!/usr/bin/env python

# This script is incrementally used to convert the index files
# from 1.csv, 2.csv ... to alphanumeric key index files a.csv, b.csv ...
# any alphanumeric index file >200MB will be further split into
# fa.csv, fb.csv, ... and so on until maximum size of any index file is
# less than 200 MB

# Import all the required packages
import os
import sys
from collections import defaultdict
import csv

def main():
    s_aindex_path = os.getcwd()+'/bwikindex/'
    s_index_path  = os.getcwd()+'/wikindex/'
    if not os.path.exists(s_aindex_path): os.makedirs(s_aindex_path)
    
    l_block_ids = [x for x in range(1, 988)]
    l_alphanum = list("abcdefghijklmnopqrstuvwxyz0123456789")
    l_alpha = list("abcdefghijklmnopqrstuvwxyz")
    l_num = list("0123456789")
    l_files = ["co", "re", "ma", "de", "in", "ca", "st", "pr", "se", "pa", "ar", "li", 
               "su", "di", "la", "po", "ch", "fi", "fo"]

'''
    for x1 in ["201"]:
        #create file handles for every digit
        print("[INFO] Processing File:", x1 + ".csv")
        d_fh = {}
        for x2 in l_num:
            d_fh[x2] = open(s_aindex_path + x1 + x2 + ".csv", "w+")

        # Splitting all the index files alphabetically
        #for n_block in l_block_ids:
        with open(s_aindex_path + x1 + ".csv", "r") as fh:
            for s_line in fh.readlines():
                if s_line[3] not in l_num:
                    continue
                else:
                    d_fh[s_line[3]].write(s_line)

        # close all the file handles
        for fh in d_fh.values():
            fh.close()
'''

'''
    for x12 in l_files:
        #create file handles for every letter
        print("[INFO] Processing File:", x12 + ".csv")
        d_fh = {}
        for x3 in l_alpha:
            d_fh[x3] = open(s_aindex_path + x12 + x3 + ".csv", "w+")

        # Splitting all the index files alphabetically
        with open(s_aindex_path + x12 + ".csv", "r") as fh:
            for s_line in fh.readlines():
                if s_line[2] not in l_alpha:
                    continue
                else:
                    d_fh[s_line[2]].write(s_line)

        # close all the file handles
        for fh in d_fh.values():
            fh.close()
'''

'''
    for x1 in l_alpha:
        #create file handles for every letter
        print("[INFO] Processing File:", x1+".csv")
        d_fh = {}
        for x2 in l_alpha:
            d_fh[x2] = open(s_aindex_path + x1 + x2 + ".csv", "w+")

        # Splitting all the index files alphabetically
        #for n_block in l_block_ids:
        with open(s_aindex_path + x1 + ".csv", "r") as fh:
            for s_line in fh.readlines():
                if s_line[1] not in l_alpha:
                    continue
                else:
                    d_fh[s_line[1]].write(s_line)

        # close all the file handles
        for fh in d_fh.values():
            fh.close()
'''

'''
    for x in l_alphanum:
        d_alpha_index = defaultdict(list)
        for n_block in l_block_ids:
            print("[INFO] [{}]Processing Block: {}".format(x, n_block))
            with open(s_index_path + str(n_block) + ".csv", "r") as fh:
                for s_line in fh.readlines():
                    if s_line[0] == x:
                        l_tokens = s_line.rstrip().split(',')
                        d_alpha_index[l_tokens[0]] += l_tokens[1:]
        print('[INFO] Creating File: {}.csv'.format(x))
        with open(s_aindex_path + x + ".csv", "w+") as f_alpha_csvfile:
            o_index_writer = csv.writer(f_alpha_csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for s_key, l_values in d_alpha_index.items():
                o_index_writer.writerow([s_key] + l_values)
'''


if __name__ == "__main__":
    main()


