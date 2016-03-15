# content of conftest.py
from collections import defaultdict
from pprint import pprint
from src.question_processing import Question_parser
oldDataHeadings = ["ArticleTitle", "Question", "Answer", "DifficultyFromQuestioner",  "DifficultyFromAnswerer",  "ArticleFile"]
dataHeadings = oldDataHeadings
def pytest_addoption(parser):
    parser.addoption("--all", action="store_true",
        help="run all combinations")

def pytest_generate_tests(metafunc):
    if 'param' in metafunc.fixturenames:
        if metafunc.config.option.all:

            questionData,questionsDataList = gen()
            questions = []

            for question in questionsDataList:
                if "NULL" not in question and "too hard" not in question and "too easy" not in question and question[3] != "NA":
                    print question
                    ques = Question_parser(question[1],difficulty = question[3],parse = False)
                    questions.append(ques)
            metafunc.parametrize("param", questions)
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
    with open('../Question_Answer_Dataset_v1.2/S10/question_answer_pairs.txt','r') as f:    
        lines = f.readlines()[1:]
        for line in lines:
            elements = line.strip().split("\t")
            questionsDataList.append(elements)
            for i in range(len(dataHeadings)):
                questionData[dataHeadings[i]].append(elements[i])
    # pprint(questionsDataList)
    return dict(questionData), questionsDataList

if __name__ == '__main__':
    gen()