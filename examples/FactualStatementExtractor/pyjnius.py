import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'
os.environ['CLASSPATH'] = "factual-statement-extractor.jar:lib/jwnl.jar:lib/stanford-parser-2008-10-26.jar:lib/commons-logging.jar:lib/commons-lang.jar"
from jnius import autoclass
from pprint import pprint
tree = "(ROOT(S(NP (NNP Francium))(VP (VBD was)(VP (VBN discovered)(PP (IN by)(NP(NP(NNP Marguerite)(NNP Perey))(PP (IN in)              (NP (NNP France)))))(PP (IN in)(NP (CD 1939)))))(. .)))"


sentence = "Star Trek is a 2009 American science fiction adventure film directed by J. J. Abrams, written by Roberto Orci and Alex Kurtzman and distributed by Paramount Pictures."
parse = autoclass("edu.cmu.ark.AnalysisUtilities").getInstance().parseSentence(sentence).parse
print parse.toString()
simp =  autoclass("edu.cmu.ark.SentenceSimplifier")()
res = simp.simplify(parse)

for i in xrange(res.size()):
    print autoclass("edu.cmu.ark.AnalysisUtilities").getCleanedUpYield(res.get(i).getIntermediateTree())
# with open("../../src/wiki.txt","r") as f:
#     data = f.readlines()
#     data = map(lambda x: unicode(x,errors ="ignore" ), data)
    
#     for sentence in data:
#         pprint(sentence)
#         print "############################"
#         parse = autoclass("edu.cmu.ark.AnalysisUtilities").getInstance().parseSentence(sentence).parse
#         print parse.toString()
#         simp =  autoclass("edu.cmu.ark.SentenceSimplifier")()
#         res = simp.simplify(parse)

#         for i in xrange(res.size()):
#             print autoclass("edu.cmu.ark.AnalysisUtilities").getCleanedUpYield(res.get(i).getIntermediateTree())
#         # break