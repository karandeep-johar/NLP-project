import sys
sys.path.append("/usr/local/lib/python2.7/site-packages")
import nltk
from init import *
from question_processing import Question_parser


def find_phrase(parse_tree,candidate_token):
	for sub_tree in parse_tree.subtrees():
		if (sub_tree.height()==3 ) and sub_tree.label()=='NP' and (set(candidate_token) <= set(sub_tree.leaves())):
			return " ".join(sub_tree.leaves())
	# If NP doesn't exist, check if a quantifier phrase exists
	qp_exists = False
	for sub_tree in parse_tree.subtrees():
		if (sub_tree.height()==3 ) and sub_tree.label()=='QP' and (set(candidate_token) <= set(sub_tree.leaves())):
			#return " ".join(sub_tree.leaves())
			qp_exists = True
			break
	min_depth = 100
    #find minimum encompassing sub-tree otherwise
    # if QP exists, return NP enclosing the QP - depth 4
	#if qp_exists == False:
	#	return []
	 # Return height 4 subtree with NP for 1) QP case 2) candidate_token is encompassed by a longer sub-tree
	for sub_tree in parse_tree.subtrees():
		if sub_tree.label()=='NP' and (set(candidate_token) <= set(sub_tree.leaves())):
			if(sub_tree.height() < min_depth):
				min_depth = sub_tree.height()

	if min_depth < 100:
		for sub_tree in parse_tree.subtrees():
			if (sub_tree.height()==min_depth) and sub_tree.label()=='NP' and (set(candidate_token) <= set(sub_tree.leaves())):
				return " ".join(sub_tree.leaves())


	return []

# Returns all depth 3 NP's encompassing Input_tags as a list
def NER_phrase_answer(Interesting_Text,questionParseObj):
	Input_tag = questionParseObj.answer_type
	question = questionParseObj.question
	question = preprocess_text(question)
	question_parsed=proc1.parse_doc(question)
	question_lemmas = question_parsed['sentences'][0]['lemmas']
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
		candidate_sentence = preprocess_text(candidate_sentence)
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
	filtered_answers = filter(lambda x: x not in question.split() and x not in question_lemmas, filtered_answers)
	print filtered_answers
	#scored_answers.append((score,filtered_answers[0]))
	#print scored_answers
	if len(filtered_answers) > 0:
		return filtered_answers[0]
	else: 
		return []

def preprocess_text(text):
	text=text.replace("-LRB-","(")
	text=text.replace("-RRB-",")")
	return text

# Returns all depth 3 NP's encompassing Input_tags as a list
def NER_phrase_utest(Interesting_Text,questionParseObj):
	Input_tag = questionParseObj.answer_type
	question = questionParseObj.question
	scored_answers = []
	print Input_tag
	#print "Person" in Input_tag
	results=[]
	candidate_sentence = Interesting_Text
	candidate_sentence = preprocess_text(candidate_sentence)
	parsed=proc1.parse_doc(candidate_sentence)
	print "Candidate sentence " , candidate_sentence
	# print parsed
	ner=parsed['sentences'][0]['ner']
	print ner
	tokens=parsed['sentences'][0]['tokens']
	candidate_token=[]
	candidate_tokens=[]
	question = preprocess_text(question)
	question_parsed=proc1.parse_doc(question)
	question_lemmas = question_parsed['sentences'][0]['lemmas']
	print question_lemmas
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
		return []
	syn_tree=parsed[u'sentences'][0][u'parse']
	parse_tree=nltk.Tree.fromstring(syn_tree)
	parse_tree.pretty_print()
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
	filtered_answers = filter(lambda x: x not in question.split() and x not in question_lemmas , filtered_answers)
	print filtered_answers
	#scored_answers.append((score,filtered_answers[0]))
	#print scored_answers
	if len(filtered_answers) > 0:
		return filtered_answers[0]
	else: 
		return []


#Unit test
if __name__ == '__main__':
	#Int_text ="I love New York and my favorite place is Bombay Delhi"
	#Input_tag="LOCATION"
	#question = "Who was Pascal's younger sister?"
	#Int_text = "Pascal had two sisters , the younger Jacqueline and the elder Gilberte ."
	#question = "When did Charles-Augustin de Coulomb join his father's family in Montpeillier?"
	#Int_text = "From 1757 to 1759 he joined his father 's family in Montpellier"
	#Int_text = "An adult paw print is approximately 10 cm -LRB- 4 inches -RRB- long."
	#question = "How long is an adult cougar's paw print?"
	#Int_text = "The pan flute was used in Greece from the 7th century BC , and spread to other parts of Europe ."
	#question = "When was the pan flute used in Greece?"
	Int_text = "Watt retired in 1800 , the same year that his fundamental patent and partnership with Boulton expired"
	question = "When did Watt retire?"
	#Int_text = preprocess_text(Int_text)
	print Int_text
	questionParseObj = Question_parser(question,parseFlag = True)
	res=NER_phrase_utest(Int_text,questionParseObj)
	print res