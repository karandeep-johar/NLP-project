import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import nltk
from init import *

def find_phrase(parse_tree,candidate_tokens):
	for sub_tree in parse_tree.subtrees():
		if (sub_tree.height()==3 ) and sub_tree.label()=='NP' and (set(candidate_tokens) <= set(sub_tree.leaves())):
			return sub_tree.leaves()
	return []

# Returns all depth 3 NP's encompassing Input_tags as a list
def NER_phrase_answer(Interesting_Text,Input_tag):
	scored_answers = []
	for i in range(len(Interesting_Text)):
		s = Interesting_Text[i]
		score = s[0]
		lemmas = s[1]['lemmas']
		posTags = s[1]['pos']
		candidate_sentence = s[1]['tokens']
		candidate_sentence = " ".join(candidate_sentence)
		#print candidate_sentence
		parsed=proc1.parse_doc(candidate_sentence)
		# print "Int text: " , Interesting_Text
		# print parsed
		# print "No. of sentences=" + str(len(parsed['sentences']))
		ner=parsed['sentences'][0]['ner']
		tokens=parsed['sentences'][0]['tokens']
		candidate_token=[]
		candidate_tokens=[]
		i=0;
		while i < len(ner):
			tag = ner[i]
			if(tag==Input_tag):
				candidate_token.append(tokens[i])
				for j in range(i+1,len(ner)):
					if(ner[j]==Input_tag):
						candidate_token.append(tokens[j])
					else:
						break
				candidate_tokens.append(candidate_token)
				candidate_token = []
				i=j
				if(j==len(ner)-1):
					break
			else:
				i = i+1
		if not candidate_tokens:
			return []

		syn_tree=parsed[u'sentences'][0][u'parse']
		parse_tree=nltk.Tree.fromstring(syn_tree)
		results=[]
		for candidate_token in candidate_tokens:
			result=find_phrase(parse_tree,candidate_token)
			results.append(result)
		#return results
		scored_answers.append((score,results))
	return scored_answers

#Unit test
if __name__ == '__main__':
	Int_text ="I love New York and my favorite place is Bombay Delhi"
	Input_tag="LOCATION"
	res=NER_phrase_answer(Int_text,Input_tag)
	print res