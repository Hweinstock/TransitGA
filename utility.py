import pickle 
from pathlib import Path 

from root_logger import RootLogger

def pickle_object(object: object, filename: str):
    if Path(filename).suffix != '.pkl':
        filename += '.pkl'
    with open(filename, 'wb') as output:
        pickle.dump(object, output)
    RootLogger.log_info(f'Succesffuly wrote object to {filename}.')

def read_object_from_file(filename: str) -> object:
    if Path(filename).suffix != '.pkl':
        RootLogger.log_warning(f'Attempting to read object from file {filename} without pickle extension.')
    with open(filename, 'rb') as input_file:
        obj = pickle.load(input_file)

    return obj