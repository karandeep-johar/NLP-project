import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import nltk
from init import *

def find_phrase(parse_tree,candidate_token):
	for sub_tree in parse_tree.subtrees():
		if (sub_tree.height()==3 ) and sub_tree.label()=='NP' and (set(candidate_token) <= set(sub_tree.leaves())):
			return " ".join(sub_tree.leaves())
	return []

# Returns all depth 3 NP's encompassing Input_tags as a list
def NER_phrase_answer(Interesting_Text,questionParseObj):
	Input_tag = questionParseObj.answer_type
	question = questionParseObj.question
	scored_answers = []
	print "No. of sentences=" + str(len(Interesting_Text))
	print Input_tag
	#print "Person" in Input_tag
	results=[]
	for i in range(1):
	#for i in range(len(Interesting_Text)):
		s = Interesting_Text[i]
		score = s[0]
		lemmas = s[1]['lemmas']
		posTags = s[1]['pos']
		candidate_sentence = s[1]['tokens']
		candidate_sentence = " ".join(candidate_sentence)
		#print candidate_sentence
		parsed=proc1.parse_doc(candidate_sentence)
		print "Candidate sentence " , candidate_sentence
		# print parsed
		ner=parsed['sentences'][0]['ner']
		print ner
		tokens=parsed['sentences'][0]['tokens']
		candidate_token=[]
		candidate_tokens=[]
		i=0;
		while i < len(ner):
			tag = ner[i]
			if tag in Input_tag:
				candidate_token.append(tokens[i])
				for j in range(i+1,len(ner)):
					if ner[j] in Input_tag:
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
			continue
		syn_tree=parsed[u'sentences'][0][u'parse']
		parse_tree=nltk.Tree.fromstring(syn_tree)
		#parse_tree.pretty_print()
		for candidate_token in candidate_tokens:
			#print candidate_token
			result=find_phrase(parse_tree,candidate_token)
			print result
			#Exclude phrases that are included in the question
			#scored_answers.append((score,filtered_answers))
			results.append(result)
		#return results
		#scored_answers.append((score,results))
	#print results
	filtered_answers = map(lambda x: str(x),results)
	filtered_answers = filter(lambda x: x not in question.split(), filtered_answers)
	print filtered_answers
	#scored_answers.append((score,filtered_answers[0]))
	#print scored_answers
	if len(filtered_answers) > 0:
		return filtered_answers[0]
	else: 
		return []

#Unit test
if __name__ == '__main__':
	Int_text ="I love New York and my favorite place is Bombay Delhi"
	Input_tag="LOCATION"
	res=NER_phrase_answer(Int_text,Input_tag)
	print res