import logging
from colorama import Fore, Style
import sys
import os
from argparse import Namespace

class RootLogger:

    verbosity_to_level = {
        0: logging.ERROR,
        1: logging.WARNING, 
        2: logging.INFO, 
        3: logging.DEBUG,
    }
    
    def initialize(path: str, verbosity: int, file_verbosity: int):
        fileHandler = logging.FileHandler(os.path.join(path, 'log.txt'), mode="w")
        fileHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s'))
        fileHandler.setLevel(level=RootLogger.verbosity_to_level[file_verbosity])

        outputHandler = logging.StreamHandler(stream=sys.stdout)
        outputHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s'))
        outputHandler.setLevel(level=RootLogger.verbosity_to_level[verbosity])

        logging.basicConfig(handlers = [fileHandler, outputHandler],
                    format='%(asctime)s, %(name)s %(levelname)s %(message)s', 
                    level=logging.NOTSET)
    
    def log_info(msg):
        logging.info(f'{Fore.BLUE}{msg}{Style.RESET_ALL}')
    
    def log_warning(msg):
        logging.warning(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')
    
    def log_debug(msg):
        logging.debug(f'{Fore.GREEN}{msg}{Style.RESET_ALL}')
    
    def log_error(msg):
        logging.error(f'{Fore.RED}{msg}{Style.RESET_ALL}')


# logging.basicConfig(filename='log.txt',
#                     filemode='w',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=RootLogger.LEVEL)