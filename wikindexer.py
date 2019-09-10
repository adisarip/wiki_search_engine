#!/usr/bin/env python

# Import all the required packages
import os
import csv
import sys
import string

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from collections import defaultdict

class WikiIndexer:
    'Indexing Wikipedia XML dump file, for search queries.'
    #n_max_doc_count = 10000 # maximum docs under each block
    # Constructor
    def __init__(self,
                 index_path_parm,
                 data_path_parm):
        self.m_stemmer = SnowballStemmer("english", ignore_stopwords=True)
        self.ml_my_stop_words = ['she', 'www', 'http', 'ref', '://']
        self.ml_stop_words = set(stopwords.words('english'))
        self.ml_stop_words.update(self.ml_my_stop_words)
        self.ml_puncts = list(string.punctuation)
        self.ms_index_path = index_path_parm
        self.ms_data_path = data_path_parm

    def getBagOfWords(self,
                      file_parm):
        # Now tokenizing and stemming the documents
        with open(file_parm, "r") as f_doc:
            s_doc_string = f_doc.read().lower()
        s_word_tokens = wordpunct_tokenize(s_doc_string)
        l_doc_bow = list()
        d_word_freq = defaultdict(int)
        for w in s_word_tokens:
            if w not in self.ml_stop_words and w not in self.ml_puncts:
                sw = self.m_stemmer.stem(w)
                if len(sw)>2:
                    l_doc_bow.append(sw)
                    d_word_freq[sw] += 1
        return l_doc_bow, d_word_freq

    # create index file
    def createIndex(self,
                    index_file_parm,
                    d_post_list_parm):
        #with open(index_file_parm, 'w+') as f_json:
        #    json.dump(d_post_list_parm, f_json)
        with open(index_file_parm, 'w+') as f_csvfile:
            o_index_writer = csv.writer(f_csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for s_key, l_values in d_post_list_parm.items():
                o_index_writer.writerow([s_key] + l_values)

    def getBlocksData(self):
        with open(self.ms_data_path+"/block.data", "r") as f_block_data:
            s_last_block, s_last_block_count = f_block_data.readline().split(",")
        n_blocks = int(s_last_block)
        n_last_block_count = int(s_last_block_count)
        return n_blocks, n_last_block_count

    # Indexing begins here
    def run(self, n_block_parm, n_docs_parm):
        d_postings_list = defaultdict(list)
        #n_blocks, n_last_block_count = self.getBlocksData()
        # Get the Bag of Words (for all documents)
        #for n_block in range(1, n_blocks+1):
        #print("[INFO] Processing Block:", n_block)
        #for n_file in range(1, WikiIndexer.n_max_doc_count+1):
        for n_file in range(1, n_docs_parm+1):
            #if (n_block == n_blocks and n_file == n_last_block_count+1):
            #    break
            s_data_file_name = str(n_block_parm) + "." + str(n_file)
            s_data_file = self.ms_data_path + str(n_block_parm) + "/" + s_data_file_name
            l_bow, d_word_freq = self.getBagOfWords(s_data_file)
            for s_term in l_bow:
                b_is_empty = True if (len(d_postings_list[s_term])) == 0 else False
                s_entry = str(d_word_freq[s_term])+":"+s_data_file_name
                if (b_is_empty):
                    d_postings_list[s_term].append(s_entry)
                else:
                    s_last_entry = d_postings_list[s_term][-1]
                    s_last_doc_id = s_last_entry.split(':')[1]
                    if (s_last_doc_id != s_data_file_name):
                        d_postings_list[s_term].append(s_entry)
        # Creating block wise index files
        s_index_file = self.ms_index_path + str(n_block_parm) + ".csv"
        self.createIndex(s_index_file, d_postings_list)
        d_postings_list.clear()

