from transit_network.transit_network import TransitNetwork 
from transit_network.stops import Stop
from transit_network.routes import SimpleRoute
from transit_network.trips import SimpleTrip
from transit_network.shapes import Coords
import genetic_algorithm.params as params
from root_logger import RootLogger

import random 
from typing import List

class Zone(Coords):
    def __init__(self, lat: float, lon: float, name: str):
        Coords.__init__(self, lat, lon)
        self.name = name 
    
    def __str__(self):
        return self.name

Z1 = Zone(params.Z1_LAT, params.Z1_LON, params.Z1_NAME)
Z2 = Zone(params.Z2_LAT, params.Z2_LON, params.Z2_NAME)
Z3 = Zone(params.Z3_LAT, params.Z3_LON, params.Z3_NAME)
Z4 = Zone(params.Z4_LAT, params.Z4_LON, params.Z4_NAME)

class ZoneEvaluator:
    
    zones = [Z1, Z2, Z3, Z4]
    zone_paths = [(Z1, Z2, 0.33), (Z3, Z2, 0.33), (Z4, Z2, 0.33)]


    def __init__(self, initial_network: TransitNetwork):
        self.initial_network = initial_network
        self.pool_of_stops = initial_network.stops 
        self.zone_keys = dict([(z, i) for i, z in enumerate(self.zones)])
        self.stops_in_zone = [self.determine_stops_in_range(z) for z in self.zones]
        self.current_stop_choices = {}
        self.initial_zone_score = 0

    def get_zone_key(self, zone: Zone) -> int:
        return self.zone_keys[zone]
    
    def get_zone_stops(self, zone: Zone) -> List[Stop]:
        zone_key = self.get_zone_key(zone)
        return self.stops_in_zone[zone_key]
    
    def determine_stops_in_range(self, zone: Zone) -> List[Stop]:
        return [s for s in self.pool_of_stops if s.distance_to_point(zone) < params.ZONE_RADIUS]
    
    def sample_stop_for_zone(self, zone: Zone): 
        stop_options = self.get_zone_stops(zone)
        # TODO: Could sample here by population weight, or by ridership weight. 
        stop_choice = random.choice(stop_options)
        return stop_choice
    
    def sample_stops(self):
        for z in self.zones:
            z_key = self.get_zone_key(z) 
            self.current_stop_choices[z_key] = self.sample_stop_for_zone(z)
        # Update initial_zone_score with new sample
        self.initial_zone_score = self.evaluate_total_zone_distance(self.initial_network)
    
    def trip_distance_to_zone(self, trip: SimpleTrip, stop_index: int, target_zone: Zone) -> int:
        trip_length = len(trip.stops)
        cur_index = stop_index
        if cur_index is None:
            return -1
        target_stops = self.get_zone_stops(target_zone)
        distance = 0 
        while cur_index < trip_length:
            if trip.stops[cur_index] in target_stops: # We have reached the target zone
                return distance 
            
            cur_index += 1
        
        return float('inf')

    def route_distance_to_zone(self, route: SimpleRoute, source_stop: Stop, target_zone: Zone) -> int:
        trip_distances = []
        if route.trips is None:
            print('heheheheheheh')
        for trip in route.trips:
            stop_index = trip.get_index_of_stop_id(source_stop.id)
            if stop_index is not None:
                trip_distances.append(self.trip_distance_to_zone(trip, stop_index, target_zone))
        if trip_distances == []:
            return float('inf')
        else:
            return min(trip_distances)


    def evaluate_zone_distance(self, target_network: TransitNetwork, source_zone: Zone, target_zone: Zone) -> float:
        source_zone_key = self.get_zone_key(source_zone)
        source_stop = self.current_stop_choices[source_zone_key]
        routes_options = source_stop.routes
        routes_dist = []
        for route_id in routes_options:
            route = target_network.lookup_route_by_id(route_id)
            if route is not None:
                route_dist = self.route_distance_to_zone(route, source_stop, target_zone)
                routes_dist.append(route_dist)

        if routes_dist == [] or min(routes_dist) == float('inf'):
            RootLogger.log_warning(f'Unable to find route from zone {source_zone}, sending distance of {params.DEFAULT_ZONE_DISTANCE}')
            return params.DEFAULT_ZONE_DISTANCE
        return min(routes_dist)

    def evaluate_total_zone_distance(self, target_network: TransitNetwork):
        total_zone_distance = 0.0

        for path in self.zone_paths:
            source_zone, target_zone, weight = path 

            dist_1 = self.evaluate_zone_distance(target_network, source_zone, target_zone)
            dist_2 = self.evaluate_zone_distance(target_network, target_zone, source_zone)
            total_zone_distance += ((dist_1 + dist_2) / 2.0)*weight

        return total_zone_distance
    
    def evaluate_network(self, target_network: TransitNetwork):
        return self.evaluate_total_zone_distance(target_network) / (self.initial_zone_score + params.ZONE_EPSILON)
                

            
    
    

    
    
        

