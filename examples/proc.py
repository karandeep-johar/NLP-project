from __future__ import absolute_import
import pprint
import logging
from stanford_corenlp_pywrapper import CoreNLP
import os
import chardet
import unicodedata
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*')
configFileLoc = os.path.join(dir, '../src/config.ini')
proc = CoreNLP(configfile=configFileLoc, corenlp_jars=[filename])
pp = pprint.PrettyPrinter(indent=2)
parsed = proc.parse_doc("Mr. Obama met Mrs. Clinton. He had spoken to her two days back.")
pp.pprint(parsed)
parsed = proc.parse_doc("Karandeep Johar, Varshaa Naganathan, Arvind Ramachandran and Dhruv Anand met to discuss the project. They had tested out Stanford CoreNLP thoroughly.")
pp.pprint(parsed)
parsed = proc.parse_doc("Is where A?")
pp.pprint(parsed)