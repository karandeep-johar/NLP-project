# content of test_compute.py
import unittest

from src.question_processing import Question_parser
def str2bool(v):
    v = ''.join( c for c in v if  c not in '?:!/;.' )
    return v.lower().strip() in ("yes", "true", "t", "1","y")
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
    questionProcess = Question_parser(param.question)
    if questionProcess.qtype != "BOOLEAN" or questionProcess.difficulty =="NA" or param.difficulty == "NA" or questionProcess.answer_type== "NA":
        return
    elif questionProcess.difficulty == "easy" and param.difficulty == "easy":
        try:
            assert True == str2bool(param.answer)
            # assert False == True
        except Exception, e:
            print param
            raise e
        
    else:
        return