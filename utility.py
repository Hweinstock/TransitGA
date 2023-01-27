import pickle 

def pickle_object(object: object, filename: str):
    with open(filename, 'wb') as output:
        pickle.dump(object, output)

def read_object_from_file(filename: str) -> object:
    with open(filename, 'rb') as input_file:
        obj = pickle.load(input_file)

    return obj