from __future__ import absolute_import
import pprint
import logging
from stanford_corenlp_pywrapper import CoreNLP
import os
dir = "."
# dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*')
configFileLoc = os.path.join(dir, 'config.ini')
proc1 = CoreNLP(configfile=configFileLoc, corenlp_jars=[filename])
proc2 = CoreNLP(configfile=os.path.join(dir, 'simple.ini'), corenlp_jars=[filename])
# proc3 = CoreNLP(configfile=os.path.join(dir, 'mid.ini'), corenlp_jars=[filename])

LOG_FILENAME = 'log.log'
LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }


logger = logging.getLogger('NLP')
#default is append
fh = logging.FileHandler(LOG_FILENAME, mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s'))

logger.addHandler(fh)
logger.info("............STARTING UP...........")
