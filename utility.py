import pickle 
import geopy.distance
from pathlib import Path 
from typing import Tuple

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

def sphere_distance(coords_1: Tuple[float, float], coords_2: Tuple[float, float]) -> float:
    # returns distance in meters. 
    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude/43211266#43211266
    km_dist = geopy.distance.geodesic(coords_1, coords_2).km 
    return km_dist * 1000
