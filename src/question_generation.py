import init
import nltk

class generateQuestions:

    def __init__(self, data, n = 1):
        self.corpus = data
        self.numQues = n
        self.questions = []
        self.generate()

    def __str__(self):
        return str(self.questions)

    def getQues(self,parsed):
        questions = []
        #print len(sub_tree.leaves())
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
            prev = -1
            for i in range(0, len(parse_tree[0])):
                if parse_tree[0,i].label() == 'NP':
                    prev = -1
                    for j in range(0, len(parse_tree[0,i])):
                        if parse_tree[0,i,j].label() == 'NP':
                            prev = 0
                        elif prev == 0:
                            if parse_tree[0,i,j].label() == ',':
                                prev = 1
                            else:
                                prev = -1
                        elif prev == 1:
                            if parse_tree[0,i,j].label() == 'NP':
                                break
                            else:
                                prev = -1
                    if prev == 1:
                        break
            if prev == 1:
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
            elif tokens[i] == "He" or tokens[i] == "She":
                questions.append('Who '+' '.join(tokens[1:]))
            elif tag[0:2] == 'NN':
                # TODO: Check for What questions first
                # TODO: Replace whole NP, not just the noun
                if ner[i] == 'PERSON':
                    questions.append('Who '+' '.join(tokens[k:]))
                elif ner[i] == 'LOCATION':
                    questions.append('Where '+' '.join(tokens[k:]))
                elif ner[i] == 'DATE':
                    questions.append('When '+' '.join(tokens[k:]))
                elif not ner[i] == ' ':
                    questions.append('What '+' '.join(tokens[k:]))
        return questions
    def get_questions(self):
        return self.questions
    def generate(self):
        proc = init.proc1
        pp = init.pprint.PrettyPrinter(indent=2)
        parsed = proc.parse_doc(self.corpus)
        # pp.pprint(parsed)
        self.questions = self.getQues(parsed)
