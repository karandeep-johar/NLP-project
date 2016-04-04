
__author__ = 'kjohar'
# The asking program: ./ask article.txt nquestions
# where article.txt is a text file containing a Wikipedia article and nquestions is an integer
# > 0 telling how many questions to generate. Output is a sequence of nquestions English
# language questions about the content of the article that a human could answer, given the
# article. Each question should be followed by a newline character. Your goal is to generate
# questions that are fluent and reasonable.
import sys
# from init import *
from question_generation import *
from sentence_transformation import *
from link_grammar import is_grammatical
def transform_question(ques):
    # TODO lone ' "Who ' company was Bad Robot Productions ."
    # TODO remove appositions 
    ques = ques.replace("``","\"")
    ques = ques.replace("''","\"")
    ques = ques.replace(" 's","'s")
    ques = ques.replace("Who's","Whose")
    return ques
# print transform_question("Who 's commander is Nero  ?")
# this whole thing takes really long on my machine. Maybe we should try a streaming model? Parallelism may help here too.
def main(args):
    if len(args)!=2:
        return
    with open(args[0], "r") as file:
        #TODO FILL ME
        data = file.read()
        #TODO clean up the file maybe like we do in answer generation
        nquestions = int(args[1])
        # TODO: Select questions
        corpus = transformSentences(data)
        # print corpus
        #because there may be sentences in the original corpus that are fine with our scheme
        qobj = generateQuestions(data+str(corpus),nquestions)
        for ques in qobj.get_questions():
            ques = transform_question(str(ques))
            if is_grammatical(ques):
                print ques
        return 
if __name__ == '__main__':
    main(sys.argv[1:])