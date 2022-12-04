import logging
from colorama import Fore, Back, Style

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class RootLogger:
    LEVEL = logging.INFO

    def log_info(msg):
        logging.info(f'{Fore.BLUE}{msg}{Style.RESET_ALL}')
    
    def log_warning(msg):
        logging.warning(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')
    
    def log_debug(msg):
        logging.debug(f'{Fore.GREEN}{msg}{Style.RESET_ALL}')
    
    def log_error(msg):
        logging.error(f'{Fore.RED}{msg}{Style.RESET_ALL}')