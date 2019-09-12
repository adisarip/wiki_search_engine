#!/usr/bin/env python

# Import all the required packages
import os
import sys
import csv
import string
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from collections import defaultdict

# WSE - Wiki Search Engine
class WSE:
    'A search engine running on wikipedia data corpus'
    #Class variables
    d_query_index = defaultdict(list)
    d_query_term_len = defaultdict(int)
    l_field_names = ['title', 'body', 'infobox', 'categories', 'ref']

    def __init__(self,
                 index_path_parm,
                 data_path_parm):
        self.ms_index_path = index_path_parm
        self.ms_data_path = data_path_parm

    # load the index file
    def loadIndex(self,
                  l_terms_parm):
        WSE.d_query_index.clear()
        WSE.d_query_term_len.clear()
        for s_term in l_terms_parm:
            s_file_name = s_term[:4] + ".csv"
            s_index_file = self.ms_index_path + s_file_name
            if not os.path.exists(s_index_file):
                s_file_name = s_term[:3] + ".csv"
                s_index_file = self.ms_index_path + s_file_name
            if not os.path.exists(s_index_file):
                s_file_name = s_term[:2] + ".csv"
                s_index_file = self.ms_index_path + s_file_name

            #print("[INFO] Loading Index File {}".format(s_file_name))
            with open(s_index_file, 'r') as f_index:
                for s_line in f_index.readlines():
                    l_tokens = s_line.rstrip().split(',')
                    if l_tokens[0] == s_term:
                        WSE.d_query_index[s_term] = l_tokens[1:]
                        WSE.d_query_term_len[s_term] = len(l_tokens) - 1
                        break

    # creating query string from search string for lookup
    def getQueryString(self,
                       search_string_parm):
        l_my_stop_words = ['she', 'www', 'http', 'ref', '://']
        l_stop_words = set(stopwords.words('english'))
        l_stop_words.update(l_my_stop_words)
        l_punct = string.punctuation
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        l_search_tokens = wordpunct_tokenize(search_string_parm)
        l_search_tokens = list(set(l_search_tokens))

        # Fix for field queries
        for s_term in WSE.l_field_names:
            try:
                l_search_tokens.remove(s_term)
            except: pass

        l_queries = list()
        for w in l_search_tokens:
            if w not in l_stop_words and w not in l_punct:
                sw = stemmer.stem(w)
                if len(sw)>2:
                    l_queries.append(sw)
        return l_queries

    # get value with the smallest key
    def getSmallestPostingListTerm(self,
                                   d_parm):
        s = ""
        if len(d_parm) == 1:
            s = list(d_parm.keys())[0]
        else:
            b_is_first_term = True
            for t in d_parm:
                if b_is_first_term == True:
                    b_is_first_term = False
                    s = t
                else:
                    s_len = d_parm[s]
                    t_len = d_parm[t]
                    if t_len < s_len:
                        s = t
        return s

    def getMergedPostingsList(self,
                              list1_parm,
                              list2_parm):
        l1 = [float(x.split(":")[1]) for x in list1_parm]
        l2 = [float(x.split(":")[1]) for x in list2_parm]
        l_rlist = list()
        p1 = p2 = 0
        while (p1 < len(list1_parm) and p2 < len(list2_parm)):
            if l1[p1] == l2[p2]:
                l_rlist.append(list1_parm[p1])
                p1 += 1
                p2 += 1
            elif l1[p1] < l2[p2]:
                p1 += 1
            else:
                p2 += 1
        return l_rlist

    # get query results
    def getQueryResult(self,
                       l_terms_parm):
        l_result = list()
        if len(l_terms_parm) == 1:
            l_result = WSE.d_query_index[l_terms_parm[0]]
        elif len(l_terms_parm) == 2:
            l_result = self.getMergedPostingsList(WSE.d_query_index[l_terms_parm[0]],
                                                  WSE.d_query_index[l_terms_parm[1]])
        else:
            s_term1 = self.getSmallestPostingListTerm(WSE.d_query_term_len)
            WSE.d_query_term_len.pop(s_term1)
            s_term2 = self.getSmallestPostingListTerm(WSE.d_query_term_len)
            WSE.d_query_term_len.pop(s_term2)

            l_result = self.getMergedPostingsList(WSE.d_query_index[s_term1],
                                                  WSE.d_query_index[s_term2])
            WSE.d_query_index.pop(s_term1)
            WSE.d_query_index.pop(s_term2)

            s_term3 = s_term1 + "_" + s_term2
            WSE.d_query_index[s_term3] = l_result
            WSE.d_query_term_len[s_term3] = len(l_result)

            self.getQueryResult(list(WSE.d_query_term_len.keys()))  # recursion
        return l_result

    # get top 'k' relevant documents
    def getKRelevantDocs(self,
                         l_doc_id_parm,
                         k_parm):
        # create the freq-DocList dictionary
        # doc list because if same frequency value linked to more than one document
        d_query_freq_doc_list = defaultdict(list)
        l_relevant = list()
        n_doc_count = 0
        for s_entry in l_doc_id_parm:
            s_freq, s_doc_id = s_entry.split(":")
            d_query_freq_doc_list[int(s_freq)].append(s_doc_id)

        l_sorted_freq = sorted(d_query_freq_doc_list.keys(), reverse=True)
        k_parm = len(l_doc_id_parm) if (len(l_doc_id_parm) < k_parm) else k_parm

        for fq in l_sorted_freq:
            for entry in d_query_freq_doc_list[fq]:
                if (n_doc_count < k_parm):
                    l_relevant.append(entry)
                    n_doc_count += 1
                else:
                    break
            if(n_doc_count >= k_parm):
                break
        return l_relevant

    # Search starts here
    def run(self, search_query_parm):
        d_relevant_files = defaultdict(list)
        l_terms = self.getQueryString(search_query_parm.lower())

        # load the wiki index
        self.loadIndex(l_terms)

        l_result_docs = self.getQueryResult(l_terms)
        d_relevant_files[search_query_parm] = self.getKRelevantDocs(l_result_docs, 10)
        return d_relevant_files
