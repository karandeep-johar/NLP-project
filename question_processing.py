from init import *


class Question_parser:

    def __init__(self, question):
        self.valid = False
        self.qtype = "NA"
        self.answer_type = "NA"
        self.difficulty = "NA"
        self.question = question
        self.parse()

    def __str__(self):
        return '\n' + self.question + "\n" +\
            "Validity= " + str(self.valid) + '\n' +\
            "Question Type = " + self.qtype + '\n' +\
            "Answer Type = " + self.answer_type + '\n' +\
            "Difficulty = " + self.difficulty + '\n'

    def parse(self):
        parsed = proc.parse_doc(self.question)
        if parsed[u'sentences'][0][u'tokens'][-1] == '?':
            self.valid = True
            first_word = parsed[u'sentences'][0][u'lemmas'][0]
            if first_word == 'be' or first_word == 'do':
                self.qtype = 'YesNo'
                self.difficulty = 'Easy'
                self.answer_type = "YesNo"
            else:
                self.qtype = "Factoid"
                self.difficulty = 'Medium'
                wh_word = parsed[u'sentences'][0][u'tokens'][0]
                if wh_word.lower() == 'who':
                    self.answer_type = "person"
                elif wh_word.lower() == 'when':
                    self.answer_type = "time"
                elif wh_word.lower() == 'where':
                    self.answer_type = "place"
                elif wh_word.lower() == 'what':
                    self.answer_type = "unknown"	 				#
                else:
                    self.answer_type = "unknown"
            # Find headword in Noun-phrase after Wh word
            # print str(parsed[u'sentences'][0][u'parse'])

question1 = "Did United defeat Chelsea"
q1_parse = Question_parser(question1)
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


#pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(parsed)
# print parsed)
# print parsed.keys()
#	print "Yes, it is question"
# Is it a yes/no question:

#		print "Yes-No"
# Invoke TFIDF and if score is high- Easy
# else hard
#	else:
#		print "Factoid"
# Find type of factoid # CHeck wh word

#
# else:
#	print "No, not a question"
# pp.pprint(parsed)
