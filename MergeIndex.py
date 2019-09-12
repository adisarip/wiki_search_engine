#!/usr/bin/env python

# This script is incrementally used to convert the index files
# from 1.csv, 2.csv ... to alphanumeric key index files a.csv, b.csv ... 0.csv, 1.csv
# any alphanumeric index file >200MB will be further split into
# fa.csv, fb.csv, ... 00.csv, 01.csv, ... and so on until maximum size of any index file is
# less than 200 MB

# Import all the required packages
import os
import sys
from collections import defaultdict
import csv
import shutil

def splitAlpha(index_parm, index_file_name_parm, index_path_parm, bkp_path_parm):
    # Split the alphabet index files recursively
    # to make sure that each individual index file size is < 200 MB
    print("[INFO] Processing File:", index_file_name_parm)
    
    # create file handles for every letter
    s_file_key = index_file_name_parm.split(".")[0]
    d_fh = {}
    for x in l_alpha:
        d_fh[x] = open(index_path_parm + s_file_key + x + ".csv", "w+")

    # Splitting the index file lexically
    with open(index_path_parm + index_file_name_parm, "r") as fh:
        for s_line in fh.readlines():
            if s_line[index_parm] not in l_alpha:
                continue
            else:
                d_fh[s_line[index_parm]].write(s_line)

    # close all the file handles
    for fh in d_fh.values():
        fh.close()

    # move the parent file into backup directory
    s_source_file = index_path_parm + index_file_name_parm
    s_dest_file = bkp_path_parm + index_file_name_parm
    shutil.move(s_source_file, s_dest_file)


def splitNum(index_parm, index_file_name_parm, index_path_parm, bkp_path_parm):
    # Split the numeric index files recursively
    # to make sure that each individual index file size is < 200 MB
    print("[INFO] Processing File:", index_file_name_parm)
    
    # create file handles for every letter
    s_file_key = index_file_name_parm.split(".")[0]
    d_fh = {}
    for x in l_num:
        d_fh[x] = open(index_path_parm + s_file_key + x + ".csv", "w+")

    # Splitting the index file lexically
    with open(index_path_parm + index_file_name_parm, "r") as fh:
        for s_line in fh.readlines():
            if s_line[index_parm] not in l_num:
                continue
            else:
                d_fh[s_line[index_parm]].write(s_line)

    # close all the file handles
    for fh in d_fh.values():
        fh.close()

    # move the parent file into backup directory
    s_source_file = index_path_parm + index_file_name_parm
    s_dest_file = bkp_path_parm + index_file_name_parm
    shutil.move(s_source_file, s_dest_file)

def main():
    s_index_path  = os.getcwd()+'/wikindex/'
    s_bkp_path = os.getcwd()+'/wikindex/bkp/'
    if not os.path.exists(s_bkp_path): os.makedirs(s_bkp_path)

    l_alphanum = list("abcdefghijklmnopqrstuvwxyz0123456789")
    l_alpha = list("abcdefghijklmnopqrstuvwxyz")
    l_num = list("0123456789")

    (_, _, l_blockfiles) = next(os.walk(s_index_path))
    # Split the block index files into alphanumeric index
    for x in l_alphanum:
        d_alpha_index = defaultdict(list)
        for n_block in l_blockfiles:
            print("[INFO] [{}]Processing: {}".format(x, n_block))
            s_block_index_file = s_index_path + str(n_block) + ".csv"
            with open(s_block_index_file, "r") as fh:
                for s_line in fh.readlines():
                    if s_line[0] == x:
                        l_tokens = s_line.rstrip().split(',')
                        d_alpha_index[l_tokens[0]] += l_tokens[1:]
        print('[INFO] Creating File: {}.csv'.format(x))
        s_index_file = s_index_path + x + ".csv"
        with open(s_index_file, "w+") as f_alpha_csvfile:
            o_index_writer = csv.writer(f_alpha_csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for s_key, l_values in d_alpha_index.items():
                o_index_writer.writerow([s_key] + l_values)
    
    # move the block index files to bkp
    for s_block_index_file in l_blockfiles:
        s_source_file = s_index_path + s_block_index_file
        s_dest_file = s_bkp_path + s_block_index_file
        shutil.move(s_source_file, s_dest_file)

    n_index = 1
    while (True):
        # now recursively get the list of files in the index directory
        (_, _, l_filenames) = next(os.walk(s_index_path))
        l_big_files = []
        for s_file_name in l_filenames:
            s_file = s_index_path + s_file_name
            n_file_size_mb = os.path.getsize(s_file) / 1048576
            if n_file_size_mb > 200:
                l_big_files.append(s_file_name)
        if len(l_big_files) == 0:
            break
        else:
            for s_file_name in l_big_files:
                s_file = s_index_path + s_file_name
                if s_file_name[0] in l_alpha:
                    splitAlpha(n_index, s_file_name, s_index_path, s_bkp_path)
                else:
                    splitNum(n_index, s_file_name, s_index_path, s_bkp_path)
        n_index += 1


if __name__ == "__main__":
    main()


