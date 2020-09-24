 # Set up a logging object
import logging
import os

cwd = os.getcwd()

logging.basicConfig(
     level = logging.DEBUG,
     filename = f"cool_parser/output_parser/parselog.txt",
     filemode = "w",
     format = "%(filename)10s:%(lineno)4d:%(message)s"
 )
log = logging.getLogger()
