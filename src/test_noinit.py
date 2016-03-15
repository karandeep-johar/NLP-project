import sys
import os
sys.path.append("/usr/local/lib/python2.7/site-packages")
import nltk
from stanford_corenlp_pywrapper import CoreNLP
from question_processing import Question_parser
import pprint
#from nltk.parse.stanford import StanfordParser
dir = "."
# dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*')
configFileLoc = os.path.join(dir, 'mid.ini')
proc1 = CoreNLP(configfile=configFileLoc, corenlp_jars=[filename])
proc=proc1
pp = pprint.PrettyPrinter(indent=2)
question = "Did Ronaldo score the last goal in the world cup?"
question_parsed=Question_parser(question,proc)
parsed=proc.parse_doc(question)
pp.pprint(parsed)
syn_tree=parsed[u'sentences'][0][u'parse']
parse_tree=nltk.Tree.fromstring(syn_tree)
print type(parse_tree)
for t in parse_tree:
	print t.constituents()
