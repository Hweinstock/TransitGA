from typing import List 

from transit_network.routes import GTFSRoute
from transit_network.stops import Stop
from root_logger import RootLogger

TRANSFER_THRESHOLD = 0.0001

def flatten(lst: List[List[any]]) -> List[any]:
    return [item for sublist in lst for item in sublist]

def should_merge(stopA: Stop, stopB: Stop) -> bool:
    if stopA.get_id() == stopB.get_id():
        RootLogger.log_debug(f'Found stops with same id, merging them.')
        return True 
    
    distance = stopA.distance_to_stop(stopB)

    if distance < TRANSFER_THRESHOLD:
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
    
    new_stops = merge_stops(all_stops)

    return new_stops 

# def determine_transfers(routes: List[GTFSRoute]):
#     # temp_all_stops = flatten([r.get_all_stops() for r in routes])
    
#     # temp_new_stops = merge_stops(temp_all_stops)
#     # print(temp_new_stops)
#     # Determine Transfers for each route
#     all_stop_transfers = {}
#     for route in routes:
#         route_stops = route.get_all_stops()
#         for stop in route_stops:
#             stop_id = stop.get_id()
#             # Already seen this stop
#             if stop_id in all_stop_transfers:
#                 stop_obj = all_stop_transfers[stop_id]
#                 # noticed that stop_id were duplicated. 
#                 # Wnder if this is because routes in two directions repeat stops on way back?
#                 if stop_id not in stop_obj.routes:
#                     RootLogger.log_info(f'Found transfer at stop {stop_id} on route {route.id}.')
#                     stop_obj.add_transfer_route(route.id)
#             else:
#                 all_stop_transfers[stop.id] = stop
#                 stop.add_transfer_route(route.id)

#     return all_stop_transfers