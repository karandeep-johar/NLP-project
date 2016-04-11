import os
from subprocess import *
#import jnius_config
#os.environ['PATH'] = os.environ['PATH'] + os.pathsep + "/Users/varshaa/Dropbox/Backups/CMU/Acads/11611/Project/NLP-project/FactualStatementExtractor"
#jnius_config.set_classpath('.', '/Users/varshaa/Dropbox/Backups/CMU/Acads/11611/Project/NLP-project/FactualStatementExtractor/src/*')
#os.environ['CLASSPATH'] = "../FactualStatementExtractor/factual-statement-extractor.jar:../FactualStatementExtractor/lib/jwnl.jar:../FactualStatementExtractor/lib/stanford-parser-2008-10-26.jar:../FactualStatementExtractor/lib/commons-logging.jar:../FactualStatementExtractor/lib/commons-lang.jar"
from jnius import autoclass
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
        f = open('transformed.txt','w')
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
            else:
                f.write(s+'\n')
        f.close()
    
    '''

    def transform(self):
        for sentence in self.corpus:
            parse = autoclass("edu.cmu.ark.AnalysisUtilities").getInstance().parseSentence(sentence).parse
            simp =  autoclass("edu.cmu.ark.SentenceSimplifier")()
            res = simp.simplify(parse)
            for i in xrange(res.size()):
                self.sentences = autoclass("edu.cmu.ark.AnalysisUtilities").getCleanedUpYield(res.get(i).getIntermediateTree())
        print "-----------BLAH------------"
        print self.sentences
    '''
