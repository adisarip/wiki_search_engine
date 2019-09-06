#!/usr/bin/env python

# Import all the required packages
import csv
import string
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from collections import defaultdict

class WikiIndexer:
    'Indexing Wikipedia XML dump file, for search queries.'

    # Constructor
    def __init__(self,
                 index_file_parm):
        self.m_stemmer = SnowballStemmer("english", ignore_stopwords=True)
        self.ml_my_stop_words = ['she', 'www', 'http', 'ref', '://']
        self.ml_stop_words = set(stopwords.words('english'))
        self.ml_stop_words.update(self.ml_my_stop_words)
        self.ml_puncts = string.punctuation
        self.ms_index_file = index_file_parm

    def getBagOfWords(self,
                      data_parm):
    # Now tokenizing and stemming the documents
    #def get_bag_of_words(data):
        #docFH = open(file)
        #docString = docFH.read()
        #docFH.close()
        s_doc_string = data_parm.lower()
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
    def createIndexFile(self,
                        post_list_parm):
        with open(self.ms_index_file, 'w+') as f_csvfile:
            o_index_writer = csv.writer(f_csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for s_key, l_values in post_list_parm.items():
                o_index_writer.writerow([s_key] + l_values)
    
    # Indexing begins here
    def run(self, d_bow_parm):
        l_postings_list = defaultdict(list)
        # Get the Bag of Words (for all documents)
        l_files = list(d_bow_parm.keys())
        for file in l_files:
            #bagOfWords = get_bag_of_words(dataFilesPath+file)
            l_bow, d_word_freq = self.getBagOfWords(d_bow_parm[file])
            for s_term in l_bow:
                b_is_empty = True if (len(l_postings_list[s_term])) == 0 else False
                s_entry = str(d_word_freq[s_term])+":"+file
                if (b_is_empty):
                    l_postings_list[s_term].append(s_entry)
                else:
                    s_last_entry = l_postings_list[s_term][-1]
                    s_last_doc_id = s_last_entry.split(':')[1]
                    if (s_last_doc_id != file):
                        l_postings_list[s_term].append(s_entry)
            d_bow_parm.pop(file)
        #Creating the Index File
        self.createIndexFile(l_postings_list)

