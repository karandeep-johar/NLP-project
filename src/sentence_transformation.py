from subprocess import *
# system for extracting simplified factual statements from complex sentences. 
# The system utilizes a set of Tregex tree searching rules to identify, 
# in phrase structure trees for input sentences, 
# instances of various constructions (e.g., relative clauses, participial phrases). 
# It then extracts simplified declarative sentences from these constructions.
class transformSentences:

    def __init__(self, data):
        self.corpus = data
        self.sentences = []
        self.transform()

    def __str__(self):
        return ' '.join(self.sentences)

    def transform(self):
        dir = "../examples/FactualStatementExtractor/"
        op = Popen(["java", "-Xmx1500m", "-cp", "factual-statement-extractor.jar:lib/jwnl.jar:lib/stanford-parser-2008-10-26.jar:lib/commons-logging.jar:lib/commons-lang.jar","edu/cmu/ark/SentenceSimplifier"],
        cwd = dir,
        stdout = PIPE,
        stdin  = PIPE,
        stderr = STDOUT)
        res = op.communicate(input=self.corpus)[0]
        self.sentences = res.split('\n')[4:-2]
        for s in self.sentences:
            if s.find("parsing") == 0:
                self.sentences.remove(s)

