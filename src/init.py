from __future__ import absolute_import
import pprint
import logging
from stanford_corenlp_pywrapper import CoreNLP
import os
# dir = "."
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*')
configFileLoc = os.path.join(dir, 'config.ini')
proc1 = CoreNLP(configfile=configFileLoc, corenlp_jars=[filename])
proc2 = CoreNLP(configfile=os.path.join(dir, 'simple.ini'), corenlp_jars=[filename])
proc3 = CoreNLP(configfile=os.path.join(dir, 'mid.ini'), corenlp_jars=[filename])
puncTags = ['.',',','IN','#','$','CC','SYM','-LRB-','-RRB-',"''",'``',"'","`",'"',':',';','[',']','{','}','-','_','!','?','~','&','*']
LOG_FILENAME = 'log.log'
LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }

MIN_PARA_SIZE = 4
def removeHeadings(article):
    data = article.read()
    data = str(unicode(data, errors='ignore'))
    splitData = data.split('\n')
    title = ' '.join(splitData[0].split('_'))+'.'
    finalParas = []
    for para in splitData:
        if len(para.split())>MIN_PARA_SIZE:
            finalParas.append(para)
    data = '\n'.join(finalParas)
    titleLemmas = [w.lower() for w in proc2.parse_doc(title)['sentences'][0]['lemmas']]
    titleLemmasSet = set(titleLemmas)
    for tL in titleLemmas:
        parts = tL.split('_')
        if len(parts)>1:
            titleLemmasSet|=set(parts)
    return data,titleLemmasSet
logger = logging.getLogger('NLP')
#default is append
fh = logging.FileHandler(LOG_FILENAME, mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'))

logger.addHandler(fh)
logger.info("............STARTING UP...........")
