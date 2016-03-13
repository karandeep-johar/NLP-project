import pprint
import logging
from stanford_corenlp_pywrapper import CoreNLP
proc1 = CoreNLP(configfile='config.ini', corenlp_jars=["../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*"])
proc2 = CoreNLP(configfile='simple.ini', corenlp_jars=["../stanford-corenlp-python/stanford-corenlp-full-2014-08-27/*"])

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
