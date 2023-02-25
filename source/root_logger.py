import logging
from colorama import Fore, Back, Style
import sys

class RootLogger:
    console_level = logging.INFO
    file_level = logging.DEBUG

    logging_format = logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s')
    fileHandler = logging.FileHandler("log.txt", mode="w")
    fileHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s %(levelname)s %(message)s'))
    fileHandler.setLevel(level=file_level)

    outputHandler = logging.StreamHandler(stream=sys.stdout)
    outputHandler.setFormatter(logging_format)
    outputHandler.setLevel(level=console_level)
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