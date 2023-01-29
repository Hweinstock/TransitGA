from typing import List 

from transit_network.routes import GTFSRoute
from transit_network.stops import Stop
from root_logger import RootLogger
from preprocessing.params import STOP_TRANSFER_THRESHOLD

def flatten(lst: List[List[any]]) -> List[any]:
    return [item for sublist in lst for item in sublist]

def should_merge(stopA: Stop, stopB: Stop) -> bool:
    if stopA.get_id() == stopB.get_id():
        RootLogger.log_debug(f'Found stops with same id, merging them.')
        return True 
    
    distance = stopA.distance_to_stop(stopB)

    if distance < STOP_TRANSFER_THRESHOLD:
        RootLogger.log_debug(f'Found stops within distance {distance}, merging them.')
        return True 
    
    return False

def merge_stops(stops: List[Stop]) -> List[Stop]:

    def merge_stop_step(cur_stop: Stop, other_stops: List[Stop]):
        remaining_stops = []
        for stop in other_stops:
            if should_merge(cur_stop, stop):
                cur_stop = cur_stop.merge_with(stop)
            else:
                remaining_stops.append(stop)
        return cur_stop, remaining_stops

    cur_stops = [s for s in stops]
    new_stops = []
    while cur_stops != []:
        RootLogger.log_debug(f'Merging stops with {len(cur_stops)} remaining.')
        cur_stop = cur_stops[0]
        new_stop, other_stops = merge_stop_step(cur_stop, cur_stops[1:])
        new_stops.append(new_stop)
        cur_stops = other_stops
    RootLogger.log_info(f'Finished merging stops, went from {len(stops)} to {len(new_stops)}.')
    return new_stops

def new_determine_transfers(routes: List[GTFSRoute]):
    all_stops = flatten([r.get_all_stops() for r in routes])

    RootLogger.log_info(f'Looking for duplicate stops across routes, starting with {len(all_stops)}')
    unique_stops_map = {}
    for stop in all_stops:
        if stop.id not in unique_stops_map:
            unique_stops_map[stop.id] = stop
        else:
            unique_stops_map[stop.id].add_transfer_routes(stop.routes)
    
    unique_stops = list(unique_stops_map.values())
    RootLogger.log_info(f'Finished looking for duplicate stops across routes, ended with {len(unique_stops)}')


    RootLogger.log_info(f'Merging stops, starting with {len(unique_stops)}')
    new_stops = merge_stops(unique_stops)
    RootLogger.log_info(f'Finished merging stops, down to {len(new_stops)}')

    return new_stops 