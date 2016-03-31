# content of test_compute.py
import unittest
import traceback
from src.question_processing import Question_parser
from src.easy import *
from src.tfidf import *
from src.answer import *
def str2bool(v):
    v = ''.join( c for c in v if  c not in '?:!/;.' )
    # return v.lower().strip()[:2] in ("no", "false", "f", "0","n")
    return v.lower().strip()[:3] in ("yes", "true", "t", "1","y","yeah")
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
    qpobj = param[0]
    stopLemmasSet = getStopLemmas()
    objTfidf,titleLemmasSet = param[1]
    questionProcess = Question_parser(qpobj.question)
    # if questionProcess.qtype != "BOOLEAN" or questionProcess.difficulty =="NA" or qpobj.difficulty == "NA" or questionProcess.answer_type== "NA":
    #     return
    if questionProcess.valid: #questionProcess.difficulty == "easy" :
        try:
            interestingText = objTfidf.getInterestingText(qpobj.question)
            ans = answerYesNo(qpobj.question, interestingText, questionProcess, titleLemmasSet,stopLemmasSet)
            # assert True == str2bool(qpobj.answer)
            assert str2bool(qpobj.answer)== str2bool(ans)
            # assert False == True
        except Exception, e:
            traceback.print_exc()
            print qpobj
            print ans
            raise e
    
    else:
        return
        
def test_factoid(param_factoid):
    qpobj = param_factoid[0]
    objTfidf = param_factoid[1]
    print objTfidf
    questionProcess = Question_parser(qpobj.question)
    if questionProcess.valid: #questionProcess.difficulty == "easy" :
        try:
            interestingText = objTfidf.getInterestingText(qpobj.question)
            ans = answerFactoid(qpobj.question, interestingText, questionProcess)
            #assert True == str2bool(qpobj.answer)
            print ans
            #assertIsNotNone(ans)
            #assert ans != None
            assert False == True
        except Exception, e:
            traceback.print_exc()
            print qpobj
            raise e
            print ans
    else:
        return