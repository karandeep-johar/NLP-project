# The answering program: ./answer article.txt questions.txt
# where article.txt is a text file containing a Wikipedia article and questions.txt is a text
# file containing questions (one per line) about the content of the article. Output is a sequence
# of answers to the questions, one per line. Your goal is to make the answers fluent, correct,
# and concise.
import sys
from init import *
from question_processing import *
from tfidf import *
from easy import *
def main(args):
    logger.critical('This message should go to the log file')
    if len(args)!=2:
        return
    with open(args[0], "r") as article , open(args[1],"r") as questions:
        data = article.read()
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
            for it in interestingText:
# <<<<<<< Updated upstream
#                 print 'IT: ' + ' '.join(it[1])
#                 # print 'IT: ' +it[3]
#             for answer in objTfidf.getAnswer(question, interestingText):
#                 print 'PA: '+answer
# =======
                # print 'IT: ' + ' '.join(it[1])
                # print 'IT: ' +it[3]
                print 'IT: ' + ' '.join(it[1])
            if "BOOLEAN" in questionParseObj.answer_type:
                print answerYesNo(question, interestingText, questionParseObj)
            # else:
            #     for answer in objTfidf.getAnswer(question, interestingText):
            #         print 'PA: '+answer
# >>>>>>> Stashed changes
            # proc = proc1
            # question1 = "Did United defeat Chelsea"
            # q1_parse = Question_parser(question1)
            # print q1_parse
if __name__ == '__main__':
    



    main(sys.argv[1:])