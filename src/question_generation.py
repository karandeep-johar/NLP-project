import init
import nltk

class generateQuestions:

    def __init__(self, data, n = 1):
        self.corpus = data
        self.numQues = n
        self.questions = []
        self.apposSentences = []
        self.generate()

    def __str__(self):
        return str(self.questions)
    
    def dealWithApposition(self, parse_tree):
        prev = -1
        s1 = []
        s2 = []
        found = 0
        for i in range(0, len(parse_tree[0])):
            if parse_tree[0,i].label() == 'NP' and found == 0:
                prev = -1
                for j in range(0, len(parse_tree[0,i])):
                    if found == 1:
                        s1.append(parse_tree[0,i,j].leaves())
                        s2.append(parse_tree[0,i,j].leaves())
                    if prev == -1:
                        if parse_tree[0,i,j].label() == 'NP':
                            prev = 0
                        else:
                            s1.append(parse_tree[0,i,j].leaves())
                            s2.append(parse_tree[0,i,j].leaves())
                    elif prev == 0:
                        if parse_tree[0,i,j].label() == ',':
                            prev = 1
                        else:
                            s1.append(parse_tree[0,i,j-1].leaves())
                            s1.append(parse_tree[0,i,j].leaves())
                            s2.append(parse_tree[0,i,j-1].leaves())
                            s2.append(parse_tree[0,i,j].leaves())
                            prev = -1
                    elif prev == 1 and found != 1:
                        if parse_tree[0,i,j].label() == 'NP':
                            s1.append(parse_tree[0,i,j-2].leaves())
                            s2.append(parse_tree[0,i,j].leaves())
                            found = 1
                        else:
                            s1.append(parse_tree[0,i,j-2].leaves())
                            s1.append(parse_tree[0,i,j-1].leaves())
                            s1.append(parse_tree[0,i,j].leaves())
                            s2.append(parse_tree[0,i,j-2].leaves())
                            s2.append(parse_tree[0,i,j-1].leaves())
                            s2.append(parse_tree[0,i,j].leaves())
                            prev = -1
            else:
                s1.append(parse_tree[0,i].leaves())
                s2.append(parse_tree[0,i].leaves())
        s1 = [str(item) for sublist in s1 for item in sublist]
        s2 = [str(item) for sublist in s2 for item in sublist]
        s1 = ' '.join(s1)
        s2 = ' '.join(s2)
        if found == 1:
            self.apposSentences.append(s1)
            self.apposSentences.append(s2)
        return found

    def getQues(self):
        proc = init.proc1
        # pp = init.pprint.PrettyPrinter(indent=2)
        parsed = proc.parse_doc(self.corpus)
        questions = []
        # print len(sub_tree.leaves())
        for s in parsed[u'sentences']:
            syn_tree=s[u'parse']
            parse_tree=nltk.Tree.fromstring(syn_tree)
            # Prune trees that are too shallow
            if parse_tree.height() < 4:
                continue
            # Left-most child should be NP
            sub_tree = parse_tree[0,0]
            k = 1
            if sub_tree.label() == 'NP':
                k = len(sub_tree.leaves())
            else:
                continue
            # Checking for apposition
            if self.dealWithApposition(parse_tree) == 1:
                continue
            pos = s[u'pos']
            ner = s[u'ner']
            parse = s[u'parse']
            tokens = s[u'tokens']
            #TODO improve this Who noted " Fate put me in the movie to show me I was talking out of my ass . ?
            tokens[-1] ="?"
            i = 0
            tag = pos[i]
            if tokens[i] == "It":
                questions.append('What '+' '.join(tokens[1:]))
            elif tag[0:2] == 'NN':
                # TODO: Check for What questions first
                # TODO: Replace whole NP, not just the noun
                if ner[i] == 'PERSON':
                    questions.append('Who '+' '.join(tokens[k:]))
                elif ner[i] == 'LOCATION':
                    questions.append('Where '+' '.join(tokens[k:]))
                elif ner[i] == 'DATE':
                    questions.append('When '+' '.join(tokens[k:]))
                else:
                    questions.append('What '+' '.join(tokens[k:]))
        return questions
            
    def get_questions(self):
        return self.questions
    
    def generate(self):
        self.questions = self.getQues()
        while len(self.apposSentences) > 0:
            self.corpus = ' '. join(self.apposSentences)
            self.apposSentences = []
            ques = self.getQues()
            for q in ques:
                self.questions.append(q)
