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
            print qpobj
            print ans
            # assert True == str2bool(qpobj.answer)
            assert str2bool(qpobj.answer)== str2bool(ans)
            # assert False == True
        except Exception, e:
            return qpobj, ans,e
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
            #assertIsNotNone(ans)
            #assert ans != None
            #assert False == True
            if qpobj.answer_type != set(['UNKNOWN']):
                condition = ans[0] in qpobj.answer
                print "evaluated condition: ", ans[0] in qpobj.answer
                print "Genereated answer ", ans[0]
                assert condition == True

        except Exception, e:
            traceback.print_exc()
            print "Ref Answer " , qpobj.answer
            print qpobj
            raise e
            print ans
    else:
        return