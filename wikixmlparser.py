#!/usr/bin/env python

# Extract Data from wikipedia xml dump file

import xml.etree.ElementTree as xtree
import string
import re
from unidecode import unidecode
from collections import defaultdict

class WikiXmlParser:
    'Parser to parse the Wiki dump XML file and create the data set'
    # Initialize member data
    def __init__(self,
                 xml_dump_file_parm,
                 data_path_parm):
        self.ms_xml_dump_file = xml_dump_file_parm
        self.ms_data_path = data_path_parm

    # Remove namespace junk and get the tag name
    def getTagName(self,
                   xml_elem_parm):
        s_tag_name = xml_elem_parm.tag
        n_idx = s_tag_name.rfind("}")
        if n_idx != -1:
            s_tag_name = s_tag_name[n_idx + 1:]
        return s_tag_name

    # Cleanup Data after tokenization
    def cleanupData(self, data_parm):
        l_chars_to_remove = list("'{}[]*;")
        s_data = unidecode(data_parm)
        s_lines = ''
        for s_line in s_data.split("\n"):
            s_regex = '[' + re.escape(''.join(l_chars_to_remove)) + ']'
            s_lines = s_lines + re.sub(s_regex, '', s_line) + "\n"
        return s_lines

    # extract data from xml dump file
    def extractXmlData(self):
        n_page_count = 0
        n_doc_count = 0
        re_clean_br_pattern = re.compile(r"</{0,}br>")
        d_bow = defaultdict(list)

        for s_event, elem in xtree.iterparse(self.ms_xml_dump_file,
                                             events=('start', 'end')):
            s_tag_name = self.getTagName(elem)
            # Collect data from all the pages
            if s_event == 'start':
                #initialize variable for each page
                if (s_tag_name == 'page'):
                    s_page_title = ''
                    s_page_id = ''
                    s_page_data = ''
                    b_is_redirect = False
                    b_is_template = False
                    b_in_revision = False
                elif s_tag_name == 'revision':
                    # Do not pick up on revision id's
                    b_in_revision = True
            else:
                if (s_tag_name == 'title'):
                    s_page_title = elem.text

                if (s_tag_name == 'id' and not b_in_revision):
                    s_page_id = str(elem.text)[2:]

                if (s_tag_name == 'redirect'):
                    b_is_redirect = True if(len(elem.attrib['title']) > 0) else False

                if (s_tag_name == 'ns'):
                    b_is_template = True if (int(elem.text) == 10) else False

                if (s_tag_name == 'text'):
                    s_page_data = str(elem.text)

                if (s_tag_name == 'page'):
                    n_page_count = n_page_count + 1
                    s_page_data_size = len(s_page_data)
                    # create a document only if it isn't a redirection or a template
                    if (not b_is_redirect and not b_is_template and s_page_data_size > 0):
                        n_doc_count = n_doc_count + 1
                        s_page_data = self.cleanupData(s_page_data)
                        s_page_data = re_clean_br_pattern.sub(" ", s_page_data)
                        #f_page = open(self.ms_data_path + s_page_id, "w")
                        f_page = open(self.ms_data_path + str(n_doc_count), "w")
                        f_page.write(s_page_title+"\n")
                        f_page.write(str(s_page_data))
                        f_page.close()
                        #d_bow[s_page_id] = s_page_data
                        d_bow[str(n_doc_count)] = s_page_data
                elem.clear()

        print ("[INFO] Number of pages read:", n_page_count)
        print ("[INFO] Number of documents created:", n_doc_count)
        return d_bow




