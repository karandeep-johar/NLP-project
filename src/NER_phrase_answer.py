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

	return None

# Returns all depth 3 NP's encompassing Input_tags as a list
def NER_phrase_answer(Interesting_Text,questionParseObj):
	Input_tag = questionParseObj.answer_type
	question = questionParseObj.question
	question = preprocess_text(question)
	question_parsed=proc1.parse_doc(question)
	question_lemmas = question_parsed['sentences'][0]['lemmas']
	question_pos = question_parsed['sentences'][0]['pos']
	question_keywords = []
	question_keywords_no_noun = []
	pos_list = ['CD','CC','JJ','JJR','JJS','NN','NNS','NNP','NNPS','RB','RBR','RBS','VB','VBD','VBG','VBN', 'VBP', 'VBZ']
	pos_list_no_noun = ['CD','CC','JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN', 'VBP', 'VBZ']
	for i in range(len(question_pos)):
		if question_pos[i] in pos_list and question_lemmas[i] not in ['be', 'do','does',"have","can","could", "will", "would"]:
		    question_keywords.append(question_lemmas[i])
		if question_pos[i] in pos_list_no_noun and question_lemmas[i] not in ['be', 'do','does',"have","can","could", "will", "would"]:
			question_keywords_no_noun.append(question_lemmas[i])

	scored_answers = []
	logger.critical( "No. of sentences=" + str(len(Interesting_Text)))
	for i in range(len(Interesting_Text)):
		s = Interesting_Text[i]
		candidate_sentence = s[1]['tokens']
		candidate_sentence = " ".join(candidate_sentence)
		logger.critical(candidate_sentence)
	sentence_found = False
	for i in range(len(Interesting_Text)):
		s = Interesting_Text[i]
		candidate_sentence = s[1]['tokens']
		candidate_sentence = " ".join(candidate_sentence)
		candidate_sentence = preprocess_text(candidate_sentence)
		parsed=proc1.parse_doc(candidate_sentence)
		ner=parsed['sentences'][0]['ner']
		tokens=parsed['sentences'][0]['tokens']
		candidate_pos=parsed['sentences'][0]['pos']
		candidate_lemmas=parsed['sentences'][0]['lemmas']
		candidate_keywords = []
		for j in range(len(candidate_pos)):
			if candidate_pos[j] in pos_list and candidate_lemmas[j] not in ['be', 'do','does',"have","can","could", "will", "would"]:
			    candidate_keywords.append(candidate_lemmas[j])
		if(len(set(candidate_keywords)&set(question_keywords)) >=1):
			sentence_found = True
			break;
	if sentence_found == False:
		return None
	logger.critical("Selected sentence is")
	logger.critical(candidate_sentence )
	logger.critical(Input_tag)
	#print "Person" in Input_tag
	results=[]
	candidate_token=[]
	candidate_tokens=[]
	i=0;
	while i < len(ner):
		tag = ner[i]
		if tag in Input_tag:
			candidate_token.append(tokens[i])
			if i == (len(ner) -1):
				candidate_tokens.append(candidate_token)
				break
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
		return None
	syn_tree=parsed[u'sentences'][0][u'parse']
	parse_tree=nltk.Tree.fromstring(syn_tree)
	#parse_tree.pretty_print()
	for candidate_token in candidate_tokens:
		#print candidate_token
		result=find_phrase(parse_tree,candidate_token)
		logger.critical(result)
		#Exclude phrases that are included in the question
		#scored_answers.append((score,filtered_answers))
		results.append(result)
		#return results
		#scored_answers.append((score,results))
	#print results
	filtered_answers = map(lambda x: str(x),results)
	filtered_answers = filter(lambda x: x not in question.split() and x.split()[0] not in question_lemmas and x != 'None', filtered_answers)
	logger.critical(filtered_answers)
	#scored_answers.append((score,filtered_answers[0]))
	#print scored_answers
	if len(filtered_answers) == 0:
		return None
	n_candidates = len(filtered_answers)
	candidate_start_words=['']*n_candidates
	candidate_start_indices=[0]*n_candidates
	candidate_distances=[0]*n_candidates
	for i in range(n_candidates):
		candidate_start_words[i] = filtered_answers[i].split()[0]
		candidate_start_indices[i] = tokens.index(candidate_start_words[i])
	remove_list = []
	question_keywords = question_keywords_no_noun	
	for i in range(len(question_keywords)):
		if question_keywords[i] not in candidate_lemmas:
			remove_list.append(question_keywords[i])
	for remove_elem in remove_list:
		question_keywords.remove(remove_elem)
	if(len(question_keywords) ==0):
		return filtered_answers[0]
	for i in range(len(question_keywords)):
		for j in range(n_candidates):
			candidate_distances[j] = candidate_distances[j]+ abs((candidate_lemmas.index(question_keywords[i])-candidate_start_indices[j]))
	best_candidate_index = candidate_distances.index(min(candidate_distances))
	return filtered_answers[best_candidate_index]

def preprocess_text(text):
	text=text.replace("-LRB-","(")
	text=text.replace("-RRB-",")")
	text=text.replace("-lrb-","(")
	text=text.replace("-rrb-",")")
	return text

# Returns all depth 3 NP's encompassing Input_tags as a list
def NER_phrase_utest(Interesting_Text,questionParseObj):
	Input_tag = questionParseObj.answer_type
	question = questionParseObj.question
	question = preprocess_text(question)
	question_parsed=proc1.parse_doc(question)
	question_lemmas = question_parsed['sentences'][0]['lemmas']
	question_pos = question_parsed['sentences'][0]['pos']
	question_keywords = []
	question_keywords_no_noun = []
	pos_list = ['CD','CC','JJ','JJR','JJS','NN','NNS','NNP','NNPS','RB','RBR','RBS','VB','VBD','VBG','VBN', 'VBP', 'VBZ']
	pos_list_no_noun = ['CD','CC','JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN', 'VBP', 'VBZ']
	#pos_list = pos_list_no_noun
	logger.critical(question_pos)
	for i in range(len(question_pos)):
		if question_pos[i] in pos_list and question_lemmas[i] not in ['be', 'do','does',"have","can","could", "will", "would"]:
		    question_keywords.append(question_lemmas[i])
		if question_pos[i] in pos_list_no_noun and question_lemmas[i] not in ['be', 'do','does',"have","can","could", "will", "would"]:
			question_keywords_no_noun.append(question_lemmas[i])
	logger.critical(question_keywords)
	scored_answers = []
	logger.critical(Input_tag)
	#print "Person" in Input_tag
	results=[]
	candidate_sentence = Interesting_Text
	candidate_sentence = preprocess_text(candidate_sentence)
	parsed=proc1.parse_doc(candidate_sentence)
	logger.critical( "Candidate sentence " )
	logger.critical(candidate_sentence)
	# print parsed
	ner=parsed['sentences'][0]['ner']
	print ner
	logger.critical(ner)
	tokens=parsed['sentences'][0]['tokens']
	candidate_pos=parsed['sentences'][0]['pos']
	candidate_lemmas=parsed['sentences'][0]['lemmas']
	candidate_keywords = []
	for i in range(len(candidate_pos)):
		if candidate_pos[i] in pos_list and candidate_lemmas[i] not in ['be', 'do','does',"have","can","could", "will", "would"]:
		    candidate_keywords.append(candidate_lemmas[i])
	logger.critical(candidate_keywords)
	if(len(set(candidate_keywords)&set(question_keywords)) < 2):
		logger.critical( "Wrong TFIDF sentence")
		return []
	candidate_token=[]
	candidate_tokens=[]
	logger.critical(question_lemmas)
	i=0;
	print "Checking all named entities"
	while i < len(ner):
		tag = ner[i]
		if tag in Input_tag:
			candidate_token.append(tokens[i])
			if i == (len(ner) -1):
				candidate_tokens.append(candidate_token)
				break
			for j in range(i+1,len(ner)):
				if ner[j] in Input_tag:
					candidate_token.append(tokens[j])
				else:
					break
			candidate_tokens.append(candidate_token)
			print candidate_token
			candidate_token = []
			i=j
			if(j==len(ner)-1):
				break
		else:
			i = i+1
	if not candidate_tokens:
		return None
	syn_tree=parsed[u'sentences'][0][u'parse']
	parse_tree=nltk.Tree.fromstring(syn_tree)
	parse_tree.pretty_print()
	for candidate_token in candidate_tokens:
		#print candidate_token
		result=find_phrase(parse_tree,candidate_token)
		logger.critical(result)
		#Exclude phrases that are included in the question
		#scored_answers.append((score,filtered_answers))
		results.append(result)
		#return results
		#scored_answers.append((score,results))
	#print results
	filtered_answers = map(lambda x: str(x),results)
	filtered_answers = filter(lambda x: x.split()[0] not in question.split() and x.split()[0] not in question_lemmas and x != 'None', filtered_answers)
	logger.critical(filtered_answers)
	#scored_answers.append((score,filtered_answers[0]))
	#print scored_answers
	print "Filtered answers"
	print filtered_answers
	if len(filtered_answers) == 0:
		return None
	n_candidates = len(filtered_answers)
	candidate_start_words=['']*n_candidates
	candidate_start_indices=[0]*n_candidates
	candidate_distances=[0]*n_candidates
	for i in range(n_candidates):
		candidate_start_words[i] = filtered_answers[i].split()[0]
		candidate_start_indices[i] = tokens.index(candidate_start_words[i])
	remove_list = []
	question_keywords = question_keywords_no_noun	
	for i in range(len(question_keywords)):
		if question_keywords[i] not in candidate_lemmas:
			remove_list.append(question_keywords[i])
	for remove_elem in remove_list:
		question_keywords.remove(remove_elem)
	if(len(question_keywords) ==0):
		return filtered_answers[0]
	for i in range(len(question_keywords)):
		for j in range(n_candidates):
			candidate_distances[j] = candidate_distances[j]+ abs((candidate_lemmas.index(question_keywords[i])-candidate_start_indices[j]))
	best_candidate_index = candidate_distances.index(min(candidate_distances))
	#for i in range(n_candidates):
	print question_keywords
	print candidate_start_words
	print candidate_distances
	return filtered_answers[best_candidate_index]


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
	#Int_text = "Watt retired in 1800 , the same year that his fundamental patent and partnership with Boulton expired"
	#question = "When did Watt retire?"
	#Int_text1 = "The copper does not react , functioning as an electrode for the reaction ."
	#Int_text1 = "In 1794 , Volta married Teresa Peregrini , with whom he raised three sons , Giovanni , Flaminio and Zanino ."
	#question = "Who did Alessandro Volta marry?"
	#question = "When did Alessandro Volta improve  and popularize the electrophorus?"
	#Int_text = "A year later , he improved and popularized the electrophorus , a device that produces a static electric charge ."
	#question = "When did Volta retire?"
	#Int_text = "Volta retired in 1819 in his estate in Camnago , a frazione of Como now called Camnago Volta after him , where he died on March 5 , 1827"
	Int_text = "In 1905 Einstein published a paper that explained the PhotoElectric effect for which he won the Nobel Prize in 1921"
	question = "When did Einstein win the Nobel prize?"
	#question = "Who showed that Avogadro's theory held in dilute solutions?"
	#Int_text = "Jacobus Henricus van ' t Hoff showed that Avogadro 's theory also held in dilute solutions ."
	#question = "What does Avogadro's Law state?"
	#Int_text = "Avogadro 's Law states that the relationship between the masses of the same volume of different gases -LRB- at the same temperature and pressure -RRB- corresponds to the relationship between their respective molecular weights ."
	Int_text = preprocess_text(Int_text)
	questionParseObj = Question_parser(question,parseFlag = True)
	res=NER_phrase_utest(Int_text,questionParseObj)
	logger.critical(type(res))
	if res and res != 'None':
	    logger.critical( "NER accepted")
	    logger.critical( "NER answer: ")
	    logger.critical(res)
	else:
		logger.critical( "NER failed: Fallback to Set-diff")
	logger.critical(res)