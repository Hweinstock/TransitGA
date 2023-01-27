import pickle 
from root_logger import RootLogger
def pickle_object(object: object, filename: str):
    full_filename = filename + '.pkl'
    with open(full_filename, 'wb') as output:
        pickle.dump(object, output)
    RootLogger.log_info(f'Succesffuly wrote object to {filename}.')

def read_object_from_file(filename: str) -> object:
    with open(filename, 'rb') as input_file:
        obj = pickle.load(input_file)

    return obj