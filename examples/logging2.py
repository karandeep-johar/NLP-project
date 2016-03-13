import logging
 
# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.INFO,filemode="w")
 
logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")