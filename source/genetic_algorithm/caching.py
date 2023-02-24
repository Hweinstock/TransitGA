from typing import List

class RouteDistanceToZoneKey:
    """An instance of solving the problem of the distance from stop_id to target_zone_name via route_id.
    """
    def __init__(self, route_id: str, stop_id: str, target_zone_name: str):
        self.route_id = route_id 
        self.stop_id = stop_id
        self.target_zone_name = target_zone_name
     
    def __str__(self):
        return f'r{self.route_id}s{self.stop_id}tz{self.target_zone_name}'

class AllRouteDistancesToZoneKey:
    """An instance of solving the problem of the distance from a stop_id to some zone via any of route_options.
    """

    def __init__(self, route_options: List[str], stop_id: str, target_zone_name: str):
        self.route_options = route_options 
        self.stop_id = stop_id
        self.target_zone_name = target_zone_name
    
    def __str__(self):
        return f'ro{" ".join(self.route_options)}s{self.stop_id}tz{self.target_zone_name}'