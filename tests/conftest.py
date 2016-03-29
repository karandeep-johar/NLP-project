# content of conftest.py
# py.test -q test_compute.py -v conftest.py --yesno >temp2

from collections import defaultdict
from pprint import pprint
from src.question_processing import Question_parser
from src.tfidf import *
from src.answer import removeHeadings
def filter_useless(question):
    if "NULL" not in question and "NA" not in question and "too hard" not in question and "too easy" not in question and question[3] != "NA":
        return True
    return False
oldDataHeadings = ["ArticleTitle", "Question", "Answer", "DifficultyFromQuestioner",  "DifficultyFromAnswerer",  "ArticleFile"]

newDataHeadings = ["eam_id","qn_id" ,"article_title","base_path","qn_difficulty_by_questioner", "qn_text" ,"is_disfluent?"  , "is_bad_qn?" , "answer" , "qn_difficulty_by_answerer"]
dataHeadings = oldDataHeadings
def pytest_addoption(parser):
    parser.addoption("--factoid", action="store_true",
        help="run all combinations")
    parser.addoption("--yesno", action="store_true",
        help="run all combinations")
    # parser.addoption("--all", action="store_true",
    #    help="run all combinations")

def pytest_generate_tests(metafunc):
    if 'param' in metafunc.fixturenames:
        if metafunc.config.option.yesno:

            questionData,questionsDataList = gen()
            questions = []
            # trying to associate articles with questions
            articleFiles = list(set(questionData["ArticleFile"]))
            questionsDataList = filter(filter_useless, questionsDataList)
            article_questions = defaultdict(list)
            for question in questionsDataList:
                if "easy" == question[3]:
                    article_questions[question[5]].append(question)
            article_tfidf = {}
            for article in article_questions:
                with open(article,"r") as f:
                    data = removeHeadings(f)
                    objTfidf = TF_IDF(data, map(lambda x:x[1], article_questions[article]))
                    article_tfidf[article] = objTfidf
            for question in questionsDataList:
                if "easy" == question[3]:
                    print question
                    ques = Question_parser(question[1],difficulty = question[3], answer = question[2],parse = False)
                    questions.append((ques,article_tfidf[question[5]]))
            metafunc.parametrize("param", questions)
    elif 'param_factoid' in metafunc.fixturenames:
        if metafunc.config.option.factoid:
            questionData,questionsDataList = gen()
            questions = []
            # trying to associate articles with questions
            articleFiles = list(set(questionData["ArticleFile"]))
            questionsDataList = filter(filter_useless, questionsDataList)
            article_questions = defaultdict(list)
            for question in questionsDataList:
                if "medium" == question[3]:
                    article_questions[question[5]].append(question)
            article_tfidf = {}
            for article in article_questions:
                with open(article,"r") as f:
                    data = removeHeadings(f)
                    objTfidf = TF_IDF(data, map(lambda x:x[1], article_questions[article]))
                    article_tfidf[article] = objTfidf
            for question in questionsDataList:
                if "medium" == question[3]:
                    print question
                    ques = Question_parser(question[1],difficulty = question[3], answer = question[2],parse = False)
                    questions.append((ques,article_tfidf[question[5]]))
            metafunc.parametrize("param_factoid", questions)
    else:
        questions = []
        questions.append(Question_parser("Did United defeat Chelsea"))
        questions.append(Question_parser("Did United defeat Chelsea?"))
        questions.append(Question_parser("Have you reached home?"))
        questions.append(Question_parser("Is it raining outside?"))
        questions.append(Question_parser("Who killed John Lennon?"))
        questions.append(Question_parser("Where are they giving free food?"))
        questions.append(Question_parser("When is the concert?"))
        questions.append(Question_parser("What time is the concert?"))
        metafunc.parametrize("param", questions)


def gen():

    oldDataHeadings = ["ArticleTitle", "Question", "Answer", "DifficultyFromQuestioner",  "DifficultyFromAnswerer",  "ArticleFile"]
    dataHeadings = oldDataHeadings
    questionData = defaultdict(list)
    questionsDataList = []
    dataset_dir = "../Question_Answer_Dataset_v1.2/S10/"
    with open(dataset_dir+'question_answer_pairs.txt','r') as f: 
        lines = f.readlines()[1:]
        for line in lines:
            elements = unicode(line.strip(), errors='ignore').split("\t")
            elements[5] = dataset_dir+elements[5]+".txt"
            questionsDataList.append(elements)
            for i in range(len(dataHeadings)):
                questionData[dataHeadings[i]].append(elements[i])
            # questionData["ArticleFile"].append(dataset_dir+elements[5]+".txt")
    # pprint(questionsDataList)
    return dict(questionData), questionsDataList

if __name__ == '__main__':
    questionData,questionsDataList = gen()
    questions = []
    # trying to associate articles with questions
    articleFiles = list(set(questionData["ArticleFile"]))
    article_questions = defaultdict(list)
    for question in questionsDataList:
        article_questions[question[5]].append(question[1])
    # pprint(articleFiles)
    # gen()