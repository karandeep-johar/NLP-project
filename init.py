import pprint
from stanford_corenlp_pywrapper import CoreNLP
proc1 = CoreNLP(configfile='config.ini', corenlp_jars=["./stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*"])
proc2 = CoreNLP(configfile='simple.ini', corenlp_jars=["./stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*"])