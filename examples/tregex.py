from subprocess import *
# USE with this http://nlp.stanford.edu:8080/parser/
def tregex(text):    
    tregex_dir = "../stanford-tregex-2015-12-09/"
    # ROOT < (S < CC=conj)
    # ROOT < (S < (/[^,]/=adjunct$.. (/,/ $.. VP)))
    # SBAR|VP|NP=app $, /,/=lead $. /,/=trail !$ CC !$ CONJP
    # NP !< CC !< CONJP < (NP=noun $.. (/,/ $.. (NP=app $.. /,/)))
    # S=finite !>> NP|PP < NP < (VP < VBP|VB|VBZ|VBD|MD) ?< /\\./=punct
    # NP=noun > NP $.. VP=modifier
    # NP=noun > NP $.. (SBAR < S=rel !< WHADVP !< WHADJP)
    op = Popen(["java", "-mx900m", "-cp", "stanford-tregex.jar:", "edu.stanford.nlp.trees.tregex.TregexPattern", "-filter", "simple.txt",
        "NP"],
        # "NP"],
    cwd = tregex_dir,
    stdout = PIPE, 
    stdin  = PIPE,
    stderr = STDOUT)
    res = op.communicate(input=text)[0]
    return res
def tsurgeon(text):
    tregex_dir = "../stanford-tregex-2015-12-09/"
    op = Popen(["java", "-mx900m", "-cp", "stanford-tregex.jar:slf4j-simple-1.7.20.jar:slf4j-api-1.7.20.jar:", 
        "edu.stanford.nlp.trees.tregex.tsurgeon.Tsurgeon","-treeFile","/home/karan/Desktop/Sem-2/11-611/NLP_project/examples/simple.txt",
        "-po","VP < PP=prep","delete prep"],
        # "NP"],
    cwd = tregex_dir,
    stdout = PIPE, 
    stdin  = PIPE,
    stderr = STDOUT)
    res = op.communicate(input=text)[0]
    return res
    # java -mx900m -cp .:  -treeFile ../examples/simple.txt -po "VP < PP=prep" "delete prep"

text = "(ROOT(S(NP (NNP Francium))(VP (VBD was)(VP (VBN discovered)(PP (IN by)(NP(NP(NNP Marguerite)(NNP Perey))(PP (IN in)              (NP (NNP France)))))(PP (IN in)(NP (CD 1939)))))(. .)))"
print tregex(text)

print tsurgeon(text)