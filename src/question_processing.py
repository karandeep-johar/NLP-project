import init
from pprint import pprint

class Question_parser:

    # def __init__(self, question):
    #     self.valid = False
    #     self.qtype = 'NA'
    #     self.answer_type = 'NA'
    #     self.difficulty = 'NA'
    #     self.question = question
    #     self.parse()
    def __init__(self, question, valid=False, qtype= 'NA', answer_type ='NA', difficulty = 'NA', answer = 'NA', parseFlag = True, article_title = 'NA', dataset = 'NA'):
        self.valid = valid
        self.qtype = qtype
        self.answer_type = answer_type
        self.difficulty = difficulty
        self.question = question
        self.answer = answer
        self.parseFlag = parseFlag
        self.article_title = article_title
        self.dataset = dataset
        if self.parseFlag == True:
            self.parse()
    def __eq__(self, other): 
            return self.__dict__ == other.__dict__
    def __cmp__(self, other): 
            return self.__dict__ == other.__dict__
    def __str__(self):
        return '\n' + self.question + '\n' +\
            'Validity= ' + str(self.valid) + '\n' +\
            'Question Type = ' + self.qtype + '\n' +\
            'Answer Type = ' + str(self.answer_type) + '\n' +\
            'Answer = ' + self.answer + '\n' +\
            'Difficulty = ' + self.difficulty + '\n' +\
            'Article_Title = ' + self.article_title + '\n' +\
            'Dataset = ' + self.dataset + '\n'

    def parse(self):
        # What can be followed by a time reference. Like on what/which date/place/person
        AUX_QWORDS = set(['be', 'do','does','have','can','could', 'will', 'would'])
        OTHER_QWORDS = set(['who','whom','when','where','how', 'what', 'why'])
        proc = init.proc1
        parsed = proc.parse_doc(self.question)
        if parsed['sentences'][0]['tokens'][-1] == '?':
            self.valid = True
            # pprint(parsed)
            wh_word=''
            lemmas =parsed['sentences'][0]['lemmas']
            wh_words = filter(lambda lemma: lemma in (AUX_QWORDS|OTHER_QWORDS), lemmas)
            wh_word = wh_words[0] if wh_words else ''
            if wh_word=='':
                self.valid = False
                return
            i = wh_words.index(wh_word)
            wh_wordL = wh_word.lower()
            if wh_wordL in AUX_QWORDS:
                self.qtype = 'BOOLEAN'
                self.difficulty = 'easy'
                self.answer_type = set(['BOOLEAN'])
            elif wh_wordL in OTHER_QWORDS:
                self.qtype = 'Factoid'
                self.difficulty = 'medium'
                if wh_wordL == 'who' or wh_wordL == 'whom':
                    self.answer_type = set(['PERSON','ORGANIZATION'])
                elif wh_wordL == 'when':
                    self.answer_type = set(['TIME','DATE'])
                elif wh_wordL == 'where':
                    self.answer_type = set(['LOCATION'])
                elif wh_wordL == 'how':
                    if parsed['sentences'][0]['tokens'][i+1].lower() not in set(['long','much','many','far']):
                        self.answer_type = set(['UNKNOWN'])
                        self.difficulty = 'hard'
                    else:
                        self.answer_type = set(['NUMBER','MONEY', 'TIME','DATE', 'PERCENT'])
                else:
                    self.difficulty = 'hard'
                    if wh_wordL == 'what':
                        self.answer_type = set(['UNKNOWN'])
                    else:
                        self.answer_type = set(['UNKNOWN'])
                
            # Why => reason
            # what => all
            # which =>all
            # Who/Whom => person/organization
            # How => number
            # When => Time/Date
            # where => location , organization
            # Find headword in Noun-phrase after Wh word
            # print str(parsed[u'sentences'][0][u'parse'])
            #TODO except how followed by is/was/do/does etc usually it is a number
            #Norway LOCATION where
            #800 NUMBER/Time/Date how
            #Anna PERSON who
            #8:30 TIME/DATE when
            #Location, Person, Organization, Money, Percent, Date, Time, Misc


if __name__ == '__main__':
    question1 = 'Does Portuguese contain words from the Arabic language?'
    q1_parse = Question_parser(question1)
    print q1_parse
    # print 'hello, it's me!'
    question2 = 'Did United defeat Chelsea?'
    q2_parse = Question_parser(question2)
    print q2_parse
    question3 = 'Have you reached home?'
    q3_parse = Question_parser(question3)
    question3 = 'Is it raining outside?'
    q3_parse = Question_parser(question3)
    print q3_parse
    question4 = 'Who killed John Lennon?'
    q4_parse = Question_parser(question4)
    print q4_parse
    question5 = 'Where are they giving free food?'
    q5_parse = Question_parser(question5)
    print q5_parse
    question6 = 'When is the concert?'
    q6_parse = Question_parser(question6)
    print q6_parse
    question7 = 'Would Karan become the president of the United States?'
    q7_parse = Question_parser(question7)
    print q7_parse
    question8 = 'In what book can I find the story of Alladin?'
    q8_parse = Question_parser(question8)
    print q8_parse
    question8 = 'Can a flute be played with several different air sources?'
    q8_parse = Question_parser(question8)
    print q8_parse
    question8 = 'Could Malay have originated from Sumatra island?'
    q8_parse = Question_parser(question8)
    print q8_parse
    
    


#pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(parsed)
# print parsed)
# print parsed.keys()
#	print 'Yes, it is question'
# Is it a yes/no question:

#		print 'Yes-No'
# Invoke TFIDF and if score is high- Easy
# else hard
#	else:
#		print 'Factoid'
# Find type of factoid # CHeck wh word

#
# else:
#	print 'No, not a question'
# pp.pprint(parsed)
