# content of test_compute.py
import unittest
import traceback
from src.question_processing import Question_parser
from src.easy import *
from src.tfidf import *
from src.answer import *
def str2bool(v):
    v = ''.join( c for c in v if  c not in '?:!/;.' )
    if v.lower().strip()[:2] in ("no", "false", "f", "0","n"):
        return False
    # if v.lower().strip()[:3] in ("yes", "true", "t", "1","y")
    return True
# def test_compute(param):
#     try:
#         assert Question_parser(param.question).difficulty == param.difficulty
#     except Exception, e:
#         print param
#         if Question_parser(param.question).answer_type=="unknown" or param.difficulty=="NA" or Question_parser(param.question).difficulty == "NA":
#             return
#         raise e
#     # assert Question_parser(param.question).difficulty == param.difficulty
def test_yesno(param):
    x = test_yesno_helper(param)
    if x:
        raise x[2]
def test_yesno_helper(yesno_param):
    __tracebackhide__ = True
    qpobj = yesno_param[0]
    stopLemmasSet = getStopLemmas()
    objTfidf,titleLemmasSet = yesno_param[1]
    questionProcess = Question_parser(qpobj.question)

    # if questionProcess.qtype != "BOOLEAN" or questionProcess.difficulty =="NA" or qpobj.difficulty == "NA" or questionProcess.answer_type== "NA":
    #     return
    if questionProcess.valid: #questionProcess.difficulty == "easy" :
        try:
            interestingText = objTfidf.getInterestingText(qpobj.question)
            ans = answerYesNo(qpobj.question, interestingText, questionProcess, titleLemmasSet,stopLemmasSet)
            print titleLemmasSet
            print qpobj
            print ans
            # assert True == str2bool(qpobj.answer)
            assert str2bool(qpobj.answer)== str2bool(ans)
            # assert False == True
        except Exception, e:
            return qpobj, ans,e

def ner_stats(correct_flag):
    ner_stats.count = ner_stats.count + 1
    if(correct_flag == True):
        ner_stats.correct = ner_stats.correct +1

ner_stats.count = 0
ner_stats.correct = 0

def ner_stats_disp():
    print "NER stats: %d out of %d" %(ner_stats.correct,ner_stats.count)

def test_factoid(param_factoid):
    qpobj = param_factoid[0]
    objTfidf = param_factoid[1]
    print objTfidf
    questionProcess = Question_parser(qpobj.question)
    if questionProcess.valid: #questionProcess.difficulty == "easy" :
        try:
            interestingText = objTfidf.getInterestingText(qpobj.question)
            ans = answerFactoid(qpobj.question, interestingText, questionProcess,objTfidf)
            #assert True == str2bool(qpobj.answer)
            #assertIsNotNone(ans)
            #assert ans != None
            #assert False == True
            #if qpobj.answer_type == set(['UNKNOWN']) and qpobj.qtype == 'Factoid':
            if qpobj.qtype == 'Factoid':
                ref_answer = qpobj.answer.lower()
                gen_answer = ans.lower()
                condition1 = gen_answer in ref_answer
                condition2 = (ref_answer in gen_answer) and (len(gen_answer.split()) - len(ref_answer.split()) <=5)
                condition = condition1 or condition2
                ner_stats(condition)
                print "evaluated condition: ", condition
                print "Genereated answer ", gen_answer
                assert False == True

        except Exception, e:
            traceback.print_exc()
            print "Ref Answer " , qpobj.answer
            print qpobj
            ner_stats_disp()
            raise e
            print ans
    else:
        return