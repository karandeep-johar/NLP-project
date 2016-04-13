
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
from spacy_generation import *
from sentence_transformation import *
from sentence_selection import *
from link_grammar import is_grammatical
from collections import defaultdict
PICKTOPK = 3
PRUNESMALL = 4

def transform_question(ques):
    # TODO lone ' "Who ' company was Bad Robot Productions ."

    ques = ques.encode('utf-8')
    ques = ques.replace("``","\"")
    ques = ques.replace("''","\"")
    ques = ques.replace(" 's","'s")
    ques = ques.replace("Who's","Whose")
    return ques

def prune_questions(questions):

    t0 = time.time()
    questions = map(transform_question, questions)
    logger.critical( "TIME transform_question took"+str(time.time()-t0))

    t0 = time.time()
    questions = map(formGrammaticalSentence, questions)
    logger.critical( "TIME formGrammaticalSentence took"+str(time.time()-t0))
    
    #pprint.pprint([questions[i] for i in range(len(questions))])
    questions = filter(lambda question: len(question.split())>PRUNESMALL, questions)
    
    questions = [q.encode('utf-8') for q in questions]
    
    t0 = time.time()
    valid_questions = filter(is_grammatical, questions)
    logger.critical( "TIME is_grammatical took"+str(time.time()-t0))
    
    #TODO Also print the original sentence from which the Question was made
    logger.critical( "ACCEPTED")
    accepted_questions = valid_questions
    logger.critical(accepted_questions)
    logger.critical("REJECTED")
    valid_questions_set = set(valid_questions)
    rejected_questions = filter(lambda question: question not in valid_questions_set, questions)
    logger.critical(rejected_questions)

    return accepted_questions, rejected_questions

def run_pipeline(sentences, nquestions ):
    
    t0 = time.time()
    qobj = generateQuestions(sentences,nquestions)
    logger.critical("TIME generateQuestions took"+str(time.time()-t0))

    t0 = time.time()
    questions = qobj.get_questions()
    questions.extend(qobj.get_easy_questions())
    logger.critical( "TIME transform_question took"+str(time.time()-t0))

    return prune_questions(questions)


# TODO look ata this issue "What : exceeded MAX_ITEMS work limit -LSB- 200000 items -RSB- ; aborting ?"
# print transform_question("Who 's commander is Nero  ?")
# this whole thing takes really long on my machine. Maybe we should try a streaming model? Parallelism may help here too.
def main(args):
    if len(args)!=2:
        return
    with open(args[0], "r") as file:
        data,_ = removeHeadings(file, True)
        #TODO clean up the file maybe like we do in answer generation
        nquestions = int(args[1])
        accepted = defaultdict(list)
        rejected = defaultdict(list)

        accepted_questions = []
        t0 = time.time()
        entities, relations = extract_entities_relations(data)
        spacy_questions = make_questions_relations(relations, entities)
        spacy_questions = [q.encode('utf-8') for q in spacy_questions]
        logger.critical( "TIME spacyQuestions took"+str(time.time()-t0))

        logger.critical( "SPACY ORIGINAL")
        logger.critical(spacy_questions)

        accepted["spacy"], rejected["spacy"] = prune_questions(spacy_questions)
        accepted_questions.extend(accepted["spacy"])

        # TODO: Select questions
        t0 = time.time()
        selObj1 = sentenceSelector(data,3)
        logger.critical("TIME sentenceSelector took"+str(time.time()-t0))
        accepted["normal"], rejected["normal"] = run_pipeline(selObj1.get_sentences(),nquestions)
        accepted_questions.extend(accepted["normal"])

        logger.critical("HARD HARD HARD")
        for question in accepted_questions:
            hqs =  make_hard_questions(question, entities, relations)        
            logger.critical(question)
            logger.critical(hqs)
            accepted["hard spacy"].extend(hqs)
        accepted_questions.extend(accepted["hard spacy"])
        logger.critical("HARD HARD HARD END")
        k = nquestions - len(accepted_questions)
        if k > 0:
            t0 = time.time()
            # corpus = transformSentences(data)
            corpus = transformSentences(selObj1.get_needTransform())
            logger.critical("TIME transformSentences took"+str(time.time()-t0))
        
            t0 = time.time()
            corpus = [q.encode('utf-8') for q in corpus]
            selObj2 = sentenceSelector(corpus,3)
            logger.critical("TIME sentenceSelector took"+str(time.time()-t0))
        
            #because there may be sentences in the original corpus that are fine with our scheme we should also pass in the original article
            accepted["fancy"], rejected["fancy"] = run_pipeline(selObj2.get_sentences(), nquestions)
            accepted_questions.extend(accepted["fancy"][:k])

        logger.critical("ACCEPTED")
        logger.critical(dict(accepted))

        logger.critical("REJECTED")
        logger.critical(dict(rejected))
        with open("generated_questions.txt", "w") as file:
            file.write("\n".join(accepted_questions))
        print "\n".join(accepted_questions)#[:nquestions]
        return 
if __name__ == '__main__':
    main(sys.argv[1:])