import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import nltk
from question_processing import Question_parser
import pprint
#from nltk.parse.stanford import StanfordParser

pp = pprint.PrettyPrinter(indent=2)
if False:
	question = "Did Ronaldo score the last goal in the world cup?"
	question_parsed=Question_parser(question,proc2)
	parsed=proc2.parse_doc(question)
	pp.pprint(parsed)
	syn_tree=parsed[u'sentences'][0][u'parse']
	parse_tree=nltk.Tree.fromstring(syn_tree)
	print type(parse_tree)
	print parse_tree

Interesting_Text="Tourism also plays an important role in Melbourne's economy, with approximately 7.6 million domestic visitors and 1.88 million international visitors in 12th july 2004."
Input_tag="DATE"
parsed=proc2.parse_doc(Interesting_Text)
#print parsed
pp.pprint(parsed)
# Get all candidate tokens with 
#print type(parsed['sentences'][0]['ner'])
ner=parsed['sentences'][0]['ner']
tokens=parsed['sentences'][0]['tokens']
candidate_tokens=[]
for i,tag in enumerate(ner):
	if(tag==Input_tag):
		candidate_tokens.append(tokens[i])
print candidate_tokens
syn_tree=parsed[u'sentences'][0][u'parse']
parse_tree=nltk.Tree.fromstring(syn_tree)
print parse_tree

# Get NP/VP just above component with candidate_tokens
print parse_tree[0]
print len(parse_tree[0])
print len(parse_tree[0][1])

parse_tree1=parse_tree
candidate_tree=[]
def find_phrase(parse_tree,candidate_tokens):
	for sub_tree in parse_tree.subtrees():
		print sub_tree.height(),sub_tree.leaves()
		if sub_tree.height()==3 and sub_tree.label()=='NP' and (set(candidate_tokens) <= set(sub_tree.leaves())):
			return sub_tree.leaves()
"""
	print "Entering function"
	print parse_tree
	print len(parse_tree)
	for i in range(len(parse_tree)):
		if(type(parse_tree[i])!=unicode):
			print "Height of subtree is %d" %(parse_tree[i].height()) 
			if(parse_tree[i].height()>=2):
				if(set(candidate_tokens) < set(parse_tree[i].leaves())):
					print "Sub-tree found"
					candidate_tree=parse_tree[i]
					print candidate_tree
					find_phrase(candidate_tree,candidate_tokens)
			elif (parse_tree[i].height==2):
				print "Candidate"
"""
result=find_phrase(parse_tree1,candidate_tokens)
print result


# Get Phrase just above 