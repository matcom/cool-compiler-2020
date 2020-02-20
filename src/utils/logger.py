 # Set up a logging object
import logging
 
logging.basicConfig(
     level = logging.DEBUG,
     filename = "src/output_parser/parselog.txt",
     filemode = "w",
     format = "%(filename)10s:%(lineno)4d:%(message)s"
 )
log = logging.getLogger()
 