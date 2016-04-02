from subprocess import *

class transformSentences:

    def __init__(self, data):
        self.corpus = data
        self.sentences = []
        self.transform()

    def __str__(self):
        return ' '.join(self.sentences)

    def transform(self):
        dir = "../FactualStatementExtractor/"
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

