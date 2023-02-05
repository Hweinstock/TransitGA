import logging
from colorama import Fore, Back, Style

class RootLogger:
    LEVEL = logging.DEBUG

    def log_info(msg):
        logging.info(f'{Fore.BLUE}{msg}{Style.RESET_ALL}')
    
    def log_warning(msg):
        logging.warning(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')
    
    def log_debug(msg):
        logging.debug(f'{Fore.GREEN}{msg}{Style.RESET_ALL}')
    
    def log_error(msg):
        logging.error(f'{Fore.RED}{msg}{Style.RESET_ALL}')

#logging.basicConfig(level=RootLogger.LEVEL)
logging.basicConfig(filename='log.txt',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=RootLogger.LEVEL)