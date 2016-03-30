__author__ = 'kjohar'
# The asking program: ./ask article.txt nquestions
# where article.txt is a text file containing a Wikipedia article and nquestions is an integer
# > 0 telling how many questions to generate. Output is a sequence of nquestions English
# language questions about the content of the article that a human could answer, given the
# article. Each question should be followed by a newline character. Your goal is to generate
# questions that are fluent and reasonable.
import sys
from init import *
from question_generation import *

def main(args):
    if len(args)!=2:
        return
    with open(args[0], "r") as file:
        #TODO FILL ME
        data = file.read()
        nquestions = int(args[1])
        quesObj = generateQuestions(data,nquestions)
        return 
if __name__ == '__main__':
    main(sys.argv[1:])