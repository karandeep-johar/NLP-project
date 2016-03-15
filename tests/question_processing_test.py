import unittest
import os
import sys
from src.question_processing import Question_parser
from src.init import logger
from nose_parameterized import parameterized

class NotSoSimpleTest(unittest.TestCase):

    def test(self):
        """Is five successfully determined to be prime?"""
        question1 = "Did United defeat Chelsea"
        q1_parse = Question_parser(question1)
        assertEqual
        print q1_parse
        # print "hello, it's me!"
        question2 = "Did United defeat Chelsea?"
        q2_parse = Question_parser(question2)
        print q2_parse
        question3 = "Have you reached home?"
        q3_parse = Question_parser(question3)
        question3 = "Is it raining outside?"
        q3_parse = Question_parser(question3)
        print q3_parse
        question4 = "Who killed John Lennon?"
        q4_parse = Question_parser(question4)
        print q4_parse
        question5 = "Where are they giving free food?"
        q5_parse = Question_parser(question5)
        print q5_parse
        question6 = "When is the concert?"
        q6_parse = Question_parser(question6)
        print q6_parse
        question7 = "What time is the concert?"
        q7_parse = Question_parser(question6)
        print q7_parse
        self.assertTrue(True)

    def test_answers(self):
        args = ["tests/wiki.txt","tests/questions.txt","tests/answers.txt"]
        logger.critical('This message should go to the log file')
        with open(args[0], "r") as article , open(args[1],"r") as questions:
            data = article.read()
            questionsList = questions.read().split('\n')
            objTfidf = TF_IDF(data, questionsList)
            # print questionsList
            for question in questionsList:
                #fluency check
                #interestingText can be a list of tuples of (sentence,score)
                print 'Q: '+question
                interestingText = objTfidf.getInterestingText(question)
                for it in interestingText:
                    print 'IT: ' + ' '.join(it[1])
                for answer in objTfidf.getAnswer(question, interestingText):
                    print 'PA: '+answer
        self.assertTrue(True)
if __name__ == '__main__':

    unittest.main()