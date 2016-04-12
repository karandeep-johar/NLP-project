import init
import nltk
# from easy_generation import *

class generateQuestions:

    def __init__(self, data, n = 1):
        self.corpus = data
        self.numQues = n
        self.questions = []
        self.apposSentences = []
        self.generate()

    def __str__(self):
        return str(self.questions)
    
    def easy_generation(self, parse_tree):
        sentence = parse_tree[0].leaves()
        sentence = [str(item) for sublist in sentence for item in sublist]
        sentence = ' '.join(sentence)
        try:
            if parse_tree[0,0].label()=='NP' and parse_tree[0,1].label()=='VP' and (parse_tree[0,1,0,0] in set(['is', 'was','does','has','can','could', 'will', 'would'])):
                word = parse_tree[0,1,0,0]
                parse_tree[0,1].remove(parse_tree[0,1,0])
                ques = word+' '+' '.join(parse_tree.leaves())
                ques = ques.split()
                ques[-1] = '?'
                print "easy_generation", ques
                if ques[1] in ["A", "An", "The"]:
                    ques[1] = ques[1].lower()
                ques = ' ' .join(ques)
                return ques
        except Exception, e:
            return None

    
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
                        found = 2
                        if not parse_tree[0,i,j].label() == ',':
                            s1.append(parse_tree[0,i,j].leaves())
                            s2.append(parse_tree[0,i,j].leaves())
                    elif found == 2:
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
                    elif prev == 1 and found == 0:
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
        if found != 0:
            self.apposSentences.append(s1)
            self.apposSentences.append(s2)
        return found

    def getQues(self):
        proc = init.proc1
        # pp = init.pprint.PrettyPrinter(indent=2)
        parsed = proc.parse_doc(self.corpus)
        questions = []
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
            sent_easy = ' '.join(tokens)
            q = self.easy_generation(parse_tree)
            if not q is None:
                questions.append(q)
            #TODO improve this Who noted " Fate put me in the movie to show me I was talking out of my ass . ?
            tokens[-1] ="?"
            i = 0
            tag = pos[i]
            if tokens[i] == "It":
                questions.append('What '+' '.join(tokens[1:]))
            elif tag[0:2] == 'NN':
                # TODO make this inverse of Question processing Even Organization should be mapped to Who 
                # TODO: Check for What questions first
                if ner[i] == 'PERSON' or ner[i] == 'ORGANIZATION':
                    questions.append('Who '+' '.join(tokens[k:]))
                elif ner[i] == 'LOCATION':
                    questions.append('Where '+' '.join(tokens[k:]))
                elif ner[i] == 'DATE' or ner[i] == 'TIME':
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
