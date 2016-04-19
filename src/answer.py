#!/usr/bin/env python
# The answering program: ./answer article.txt questions.txt
# where article.txt is a text file containing a Wikipedia article and questions.txt is a text
# file containing questions (one per line) about the content of the article. Output is a sequence
# of answers to the questions, one per line. Your goal is to make the answers fluent, correct,
# and concise.
import sys
from init import *
from question_processing import *
from NER_phrase_answer import *
from tfidf import *
from easy import *

def find_phrase_diff(parse_tree,candidate_token):
    for sub_tree in parse_tree.subtrees():
        if (sub_tree.height()==3 ) and (sub_tree.label()=='NP' or sub_tree.label()=='VP' or sub_tree.label()=='S') and (set(candidate_token) <= set(sub_tree.leaves())):
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
    #   return []
     # Return height 4 subtree with NP for 1) QP case 2) candidate_token is encompassed by a longer sub-tree
    for sub_tree in parse_tree.subtrees():
        if (sub_tree.label()=='NP' or sub_tree.label()=='VP' or sub_tree.label()=='S') and (set(candidate_token) <= set(sub_tree.leaves())):
            if(sub_tree.height() < min_depth):
                min_depth = sub_tree.height()

    if min_depth < 100:
        for sub_tree in parse_tree.subtrees():
            if (sub_tree.height()==min_depth) and (sub_tree.label()=='NP' or sub_tree.label()=='VP' or sub_tree.label()=='S') and (set(candidate_token) <= set(sub_tree.leaves())):
                return " ".join(sub_tree.leaves())
    return None


def Refine_TFIDF_answer(diff_answer,candidate_sentence_struct):
    #print "Candidate sentence: " 
    candidate_sentence = " ".join(candidate_sentence_struct['tokens'])
    #print "Diff answer: "  
    #print diff_answer
    diff_answer_parse = proc1.parse_doc(diff_answer)
    #print "POS"
    #print " ".join(diff_answer_parse['pos'])
    diff_pos_tags=diff_answer_parse['sentences'][0]['pos']
    #print diff_pos_tags
    diff_tokens=diff_answer_parse['sentences'][0]['tokens']
    diff_keywords = []
    pos_list = ['CD','CC','JJ','JJR','JJS','NN','NNS','NNP','NNPS','RB','RBR','RBS','VB','VBD','VBG','VBN', 'VBP', 'VBZ']
    for i in range(len(diff_pos_tags)):
        if diff_pos_tags[i] in pos_list:
            diff_keywords.append(diff_tokens[i])
    #print "Diff keywords"
    #print diff_keywords
    candidate_sentence = preprocess_text(candidate_sentence)
    parsed_candidate = proc1.parse_doc(candidate_sentence)
    syn_tree=parsed_candidate[u'sentences'][0][u'parse']
    parse_tree=nltk.Tree.fromstring(syn_tree)
    refined_answer = find_phrase_diff(parse_tree,diff_keywords)
    #print "Refined answer: "  
    #print refined_answer
    # Find all nouns/verbs/adjs in the 
    # Parse the diff to find Noun?
    return refined_answer

def SelectCandidateSentence(Interesting_Text,questionParseObj):
    question = questionParseObj.question
    question = preprocess_text(question)
    question_parsed=proc1.parse_doc(question)
    question_lemmas = question_parsed['sentences'][0]['lemmas']
    question_pos = question_parsed['sentences'][0]['pos']
    question_keywords = []
    pos_list = ['CD','CC','JJ','JJR','JJS','NN','NNS','NNP','NNPS','RB','RBR','RBS','VB','VBD','VBG','VBN', 'VBP', 'VBZ']
    #pos_list = ['CD','CC','JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN', 'VBP', 'VBZ']
    for i in range(len(question_pos)):
        if question_pos[i] in pos_list and question_lemmas[i] not in ['be', 'do','does',"have","can","could", "will", "would"]:
            question_keywords.append(question_lemmas[i])
    logger.critical( "No. of sentences=")
    logger.critical(str(len(Interesting_Text)))
    for i in range(len(Interesting_Text)):
        s = Interesting_Text[i]
        candidate_sentence = s[1]['tokens']
        candidate_sentence = " ".join(candidate_sentence)
        logger.critical(candidate_sentence)
    sentence_found = False
    #logger.critical("Selected sentence:")
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
            return i
    return 0


def answerFactoid(question,interestingText,questionParseObj,objTfidf):
    answers=[]
    if(questionParseObj.answer_type != set(['UNKNOWN','NA'])):
        answer = NER_phrase_answer(interestingText,questionParseObj)
        if answer and answer != 'None':
            logger.critical( "NER accepted")
            logger.critical( "NER answer: ")
            logger.critical(answer)
            answers.append(answer)
            return answers[0]
        else:
            logger.critical("NER failed: Fallback to Set-diff")
    # If NER approach fails or NER tag is not avaialable, resort to set difference method
    answerlist=objTfidf.getAnswer(question, interestingText,questionParseObj)
    sentence_index = SelectCandidateSentence(interestingText,questionParseObj)
    answer_ready = False
    while not answer_ready and (sentence_index < len(answerlist)):
        answer_processed = Refine_TFIDF_answer(answerlist[sentence_index],interestingText[sentence_index][1])
        logger.critical("Set diff answer:")
        logger.critical(answer_processed)
        if answer_processed is not None:
            answers.append(answer_processed)
            answer_ready = True
        else:
            sentence_index += 1
    if not answer_ready:
        s = Interesting_Text[0]
        candidate_sentence = s[1]['tokens']
        return " ".join(candidate_sentence)
    return answers[0]

def getStopLemmas():
    # For longer stopword list
    # stopLemmas = open('../data/StopLemmas.txt').read().split()
    stopLemmas = open('shortStopLemmas.txt').read().split()
    return set(stopLemmas)

def main(args):
    logger.critical('This message should go to the log file')
    stopLemmasSet = getStopLemmas()
    if len(args)!=2:
        return
    with open(args[0], "r") as article , open(args[1],"r") as questions:
        data,titleLemmasSet,_ = removeHeadings(article)
        questionsList = questions.read().split('\n')
        questionsList = [x for x in questionsList if x]
        objTfidf = TF_IDF(data, questionsList)
        # print questionsList
        for question in questionsList:
            #fluency check
            #interestingText can be a list of tuples of (sentence,score)
            try:
                logger.critical( 'Q: '+question)
                questionParseObj = Question_parser(question)
                interestingText = objTfidf.getInterestingText(question)
                if "BOOLEAN" in questionParseObj.answer_type:
                    print answerYesNo(question, interestingText, questionParseObj,titleLemmasSet,stopLemmasSet)
                else:
                    print formGrammaticalSentence(answerFactoid(question,interestingText,questionParseObj,objTfidf))
            except Exception, e:
                print ""


if __name__ == '__main__':
    main(sys.argv[1:])