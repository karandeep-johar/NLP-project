import sys
sys.path.append("./../")
from question_processing import *
from init import *
proc = init.proc1
if __name__ == '__main__':
    question1 = "Did United defeat Chelsea"
    q1_parse = Question_parser(proc,question1)
    print q1_parse
    # print "hello, it's me!"
    question2 = "Did United defeat Chelsea?"
    q2_parse = Question_parser(proc,question2)
    print q2_parse
    question3 = "Have you reached home?"
    q3_parse = Question_parser(proc,question3)
    question3 = "Is it raining outside?"
    q3_parse = Question_parser(proc,question3)
    print q3_parse
    question4 = "Who killed John Lennon?"
    q4_parse = Question_parser(proc,question4)
    print q4_parse
    question5 = "Where are they giving free food?"
    q5_parse = Question_parser(proc,question5)
    print q5_parse
    question6 = "When is the concert?"
    q6_parse = Question_parser(proc,question6)
    print q6_parse
    question7 = "What time is the concert?"
    q7_parse = Question_parser(proc,question6)
    print q7_parse