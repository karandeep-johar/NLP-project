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

def answerFactoid(question,interestingText,questionParseObj):
    answers=[]
    # for it in interestingText:
    #     print 'IT: ' + ' '.join(it[1])
    #     # print 'IT: ' +it[3]
    #for answer in objTfidf.getAnswer(question, interestingText,questionParseObj):
    #     print 'PA: '+answer
         #answers.append(answer)
    answer = NER_phrase_answer(interestingText,questionParseObj)
    answers.append(answer)
    #for answer in NER_phrase_answer(interestingText,questionParseObj):
        #print 'NER: '+ answer
    return answers

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
                answerFactoid(question,interestingText,questionParseObj)

if __name__ == '__main__':
    main(sys.argv[1:])