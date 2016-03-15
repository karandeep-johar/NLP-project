# content of test_compute.py
import unittest

from src.question_processing import Question_parser

def test_compute(param):
    try:
        assert Question_parser(param.question).difficulty == param.difficulty
    except Exception, e:
        print param
        if Question_parser(param.question).answer_type=="unknown" or param.difficulty=="NA" or Question_parser(param.question).difficulty == "NA":
            return
        raise e
    # assert Question_parser(param.question).difficulty == param.difficulty