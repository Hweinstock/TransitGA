from typing import List 

from transit_network.routes import GTFSRoute
from root_logger import RootLogger

def determine_transfers(routes: List[GTFSRoute]):
    # Determine Transfers for each route
    all_stop_transfers = {}
    for route in routes:
        route_stops = route.get_all_stops()
        for stop in route_stops:
            stop_id = stop.get_id()
            # Already seen this stop
            if stop_id in all_stop_transfers:
                stop_obj = all_stop_transfers[stop_id]
                # noticed that stop_id were duplicated. 
                # Wnder if this is because routes in two directions repeat stops on way back?
                if stop_id not in stop_obj.routes:
                    RootLogger.log_info(f'Found transfer at stop {stop_id} on route {route.id}.')
                    stop_obj.add_transfer_route(route.id)
            else:
                all_stop_transfers[stop.id] = stop
                stop.add_transfer_route(route.id)

    return all_stop_transfers