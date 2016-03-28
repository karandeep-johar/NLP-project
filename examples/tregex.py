from subprocess import *

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
        "/\\.*/ < CC <<NP|ADJP|VP|ADVP|PP=unmv"],
        # "NP"],
    cwd = tregex_dir,
    stdout = PIPE, 
    stdin  = PIPE,
    stderr = STDOUT)
    res = op.communicate(input=text)[0]
    return res

text = "(ROOT(S(NP (NNP Francium))(VP (VBD was)(VP (VBN discovered)(PP (IN by)(NP(NP(NNP Marguerite)(NNP Perey))(PP (IN in)              (NP (NNP France)))))(PP (IN in)(NP (CD 1939)))))(. .)))"
print tregex(text)