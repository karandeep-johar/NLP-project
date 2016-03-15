import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import nltk
from question_processing import Question_parser
import pprint
#from nltk.parse.stanford import StanfordParser

pp = pprint.PrettyPrinter(indent=2)
question = "Did Ronaldo score the last goal in the world cup?"
question_parsed=Question_parser(question,proc)
parsed=proc.parse_doc(question)
pp.pprint(parsed)
syn_tree=parsed[u'sentences'][0][u'parse']
parse_tree=nltk.Tree.fromstring(syn_tree)
print type(parse_tree)
print parse_tree