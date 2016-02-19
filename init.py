#annotators = tokenize,ssplit,pos,lemma,parse, #ner,dcoref
import pprint
from stanford_corenlp_pywrapper import CoreNLP
proc = CoreNLP(configfile='config.ini', corenlp_jars=["./stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*"])
