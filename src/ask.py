
__author__ = 'kjohar'
# The asking program: ./ask article.txt nquestions
# where article.txt is a text file containing a Wikipedia article and nquestions is an integer
# > 0 telling how many questions to generate. Output is a sequence of nquestions English
# language questions about the content of the article that a human could answer, given the
# article. Each question should be followed by a newline character. Your goal is to generate
# questions that are fluent and reasonable.
import sys
import time
import pprint
from init import *
from question_generation import *
from sentence_transformation import *
from sentence_selection import *
from link_grammar import is_grammatical
def transform_question(ques):
    # TODO lone ' "Who ' company was Bad Robot Productions ."
    # TODO remove appositions

    ques = str(ques) 
    ques = ques.replace("``","\"")
    ques = ques.replace("''","\"")
    ques = ques.replace(" 's","'s")
    ques = ques.replace("Who's","Whose")
    return ques

def run_pipeline(sentences, nquestions,  pickTopk, pruneSmall):
    
    t0 = time.time()
    # qobj = generateQuestions(data,nquestions)
    qobj = generateQuestions(sentences,nquestions)
    print "TIME generateQuestions took",time.time()-t0

    t0 = time.time()
    questions = map(transform_question, qobj.get_questions())
    print "TIME transform_question took",time.time()-t0

    t0 = time.time()
    questions = map(formGrammaticalSentence, questions)
    print "TIME formGrammaticalSentence took",time.time()-t0

    #pprint.pprint([questions[i] for i in range(len(questions))])
    questions = filter(lambda question: len(question.split())>pruneSmall, questions)

    questions = map(str, questions)
    valid = questions
    # TODO: Check for <Question Word> , rest of question ? cases and remove comma
    t0 = time.time()
    valid = map(is_grammatical, questions)
    print "TIME is_grammatical took",time.time()-t0
    
    #TODO Also print the original sentence from which the Question was made
    print "ACCEPTED"
    accepted_questions = map(lambda idx: questions[idx], filter(lambda i: valid[i], range(len(questions))))
    pprint.pprint(accepted_questions)
    print "REJECTED"
    pprint.pprint(filter(lambda question: question not in accepted_questions, questions))
    return accepted_questions

# TODO look ata this issue "What : exceeded MAX_ITEMS work limit -LSB- 200000 items -RSB- ; aborting ?"
# print transform_question("Who 's commander is Nero  ?")
# this whole thing takes really long on my machine. Maybe we should try a streaming model? Parallelism may help here too.
def main(args):
    if len(args)!=2:
        return
    with open(args[0], "r") as file:
        data,_ = removeHeadings(file)
        #TODO clean up the file maybe like we do in answer generation
        nquestions = int(args[1])
        # TODO: Select questions
        t0 = time.time()
        selObj1 = sentenceSelector(data,3)
        print "TIME sentenceSelector took",time.time()-t0
        accepted_questions = run_pipeline(selObj1.get_sentences(), nquestions ,pickTopk = 3,pruneSmall = 4)
        

        k = nquestions - len(accepted_questions)
        if k > 0:

            t0 = time.time()
            # corpus = transformSentences(data)
            corpus = transformSentences(selObj1.get_needTransform())
            print "TIME transformSentences took",time.time()-t0
        
            t0 = time.time()
            selObj2 = sentenceSelector(str(corpus),3)
            print "TIME sentenceSelector took",time.time()-t0
        
            #because there may be sentences in the original corpus that are fine with our scheme we should also pass in the original article
            accepted_questions2 = run_pipeline(selObj2.get_sentences(), nquestions ,pickTopk = 3,pruneSmall = 4)
            accepted_questions.append(accepted_questions2[:k])
    
        return 
if __name__ == '__main__':
    main(sys.argv[1:])