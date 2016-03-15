import sys
import os
sys.path.append("/usr/local/lib/python2.7/site-packages")
import nltk
# from stat_parser import Parser
from stanford_corenlp_pywrapper import CoreNLP
from question_processing import Question_parser
import pprint
#from nltk.parse.stanford import StanfordParser


pp = pprint.PrettyPrinter(indent=2)
dir = "."
# dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*')
configFileLoc = os.path.join(dir, 'mid.ini')
proc1 = CoreNLP(configfile=configFileLoc, corenlp_jars=[filename])
question = "Did Ronaldo score the last goal in the world cup?"
question_parsed=Question_parser(question,proc)
#print question_parsed
parsed=proc.parse_doc(question)
pp.pprint(parsed)
#dep_list=parsed[u'sentences'][0][u'deps_basic']
syn_tree=parsed[u'sentences'][0][u'parse']
#print type(syn_tree)
#parser = Parser()
#syntax_parse= parser.parse("When was Gandhi born?")
#print type(syntax_parse)
parse_tree=nltk.Tree.fromstring(syn_tree)
print type(parse_tree)
print parse_tree
#print parse_tree.determineHead()

#parser = StanfordParser()


#for a_list in dep_list:
#	print a_list
#parsed = proc.parse_doc(question)
#if parsed[u'sentences'][0][u'tokens'][-1] == '?':
#self.valid = True
#first_word = parsed[u'sentences'][0][u'lemmas'][0]
#if first_word == 'be' or first_word == 'do':
#	self.qtype = 'YesNo'
#	self.difficulty = 'Easy'
#	self.answer_type = "YesNo"
