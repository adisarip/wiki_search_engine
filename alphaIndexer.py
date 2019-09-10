#!/usr/bin/env python

# Import all the required packages
import os
import sys

def main():
    s_aindex_path = os.getcwd()+'/awikindex/alpha/'
    s_index_path  = os.getcwd()+'/awikindex/'
    if not os.path.exists(s_aindex_path): os.makedirs(s_aindex_path)
    
    l_block_ids = [x for x in range(1, 988)]
    l_alphanum = list("abcdefghijklmnopqrstuvwxyz0123456789")
    l_alpha = list("abcdefghijklmnopqrstuvwxyz")

    for x1 in l_alpha:
        #create file handles for every letter
        print("[INFO] Processing File:", x1+".csv")
        d_fh = {}
        for x2 in l_alpha:
            d_fh[x2] = open(s_aindex_path + x1 + x2 + ".csv", "a+")

        # Splitting all the index files alphabetically
        #for n_block in l_block_ids:
        with open(s_index_path + x1 + ".csv", "r") as fh:
            for s_line in fh.readlines():
                if s_line[1] not in l_alpha:
                    continue
                else:
                    d_fh[s_line[1]].write(s_line)

        # close all the file handles
        for fh in d_fh.values():
            fh.close()

if __name__ == "__main__":
    main()


