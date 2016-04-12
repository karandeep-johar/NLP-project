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
    return []


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
    parsed_candidate = proc1.parse_doc(candidate_sentence)
    syn_tree=parsed_candidate[u'sentences'][0][u'parse']
    parse_tree=nltk.Tree.fromstring(syn_tree)
    refined_answer = find_phrase_diff(parse_tree,diff_keywords)
    #print "Refined answer: "  
    #print refined_answer
    # Find all nouns/verbs/adjs in the 
    # Parse the diff to find Noun?
    return refined_answer

def answerFactoid(question,interestingText,questionParseObj,objTfidf):
    answers=[]
    if(questionParseObj.answer_type == set(['UNKNOWN'])):
        answerlist=objTfidf.getAnswer(question, interestingText,questionParseObj)
        answer_processed = Refine_TFIDF_answer(answerlist[0],interestingText[0][1])
        answers.append(answer_processed)
    else:
        answer = NER_phrase_answer(interestingText,questionParseObj)
        answers.append(answer)
    return answers[0]

def getStopLemmas():
    # For longer stopword list
    # stopLemmas = open('../data/StopLemmas.txt').read().split()
    stopLemmas = open('../data/shortStopLemmas.txt').read().split()
    return set(stopLemmas)

def main(args):
    logger.critical('This message should go to the log file')
    stopLemmasSet = getStopLemmas()
    if len(args)!=2:
        return
    with open(args[0], "r") as article , open(args[1],"r") as questions:
        data,titleLemmasSet = removeHeadings(article)
        questionsList = questions.read().split('\n')
        questionsList = [x for x in questionsList if x]
        objTfidf = TF_IDF(data, questionsList)
        # print questionsList
        for question in questionsList:
            #fluency check
            #interestingText can be a list of tuples of (sentence,score)
            print 'Q: '+question
            questionParseObj = Question_parser(question)
            interestingText = objTfidf.getInterestingText(question)
            if "BOOLEAN" in questionParseObj.answer_type:
                print answerYesNo(question, interestingText, questionParseObj,titleLemmasSet,stopLemmasSet)
            else:
                print formGrammaticalSentence(answerFactoid(question,interestingText,questionParseObj,objTfidf)[0])

if __name__ == '__main__':
    main(sys.argv[1:])