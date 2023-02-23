from transit_network.transit_network import TransitNetwork 
from transit_network.stops import Stop
from transit_network.routes import SimpleRoute
from transit_network.trips import SimpleTrip
from transit_network.shapes import Coords
import genetic_algorithm.params as params
from root_logger import RootLogger

import random 
from typing import List, Tuple
random.seed(10)

class Zone(Coords):
    def __init__(self, lat: float, lon: float, name: str, color: str):
        Coords.__init__(self, lat, lon)
        self.name = name 
        self.color = color
    
    def __str__(self):
        return self.name

class TransitPath:
    def __init__(self, first_zone: Zone, second_zone: Zone, weight: float):
        self.first_zone = first_zone
        self.second_zone = second_zone 
        self.weight = weight 
    
    def as_tuple(self) -> Tuple[Zone, Zone, float]:
        return (self.first_zone, self.second_zone, self.weight)

Z1 = Zone(params.Z1_LAT, params.Z1_LON, params.Z1_NAME, params.Z1_COLOR)
Z2 = Zone(params.Z2_LAT, params.Z2_LON, params.Z2_NAME, params.Z2_COLOR)
Z3 = Zone(params.Z3_LAT, params.Z3_LON, params.Z3_NAME, params.Z3_COLOR)
Z4 = Zone(params.Z4_LAT, params.Z4_LON, params.Z4_NAME, params.Z4_COLOR)
Z5 = Zone(params.Z5_LAT, params.Z5_LON, params.Z5_NAME, params.Z5_COLOR)
Z6 = Zone(params.Z6_LAT, params.Z6_LON, params.Z6_NAME, params.Z6_COLOR)
Z7 = Zone(params.Z7_LAT, params.Z7_LON, params.Z7_NAME, params.Z7_COLOR)
Z8 = Zone(params.Z8_LAT, params.Z8_LON, params.Z8_NAME, params.Z8_COLOR)
Z9 = Zone(params.Z9_LAT, params.Z9_LON, params.Z9_NAME, params.Z9_COLOR)
Z10 = Zone(params.Z10_LAT, params.Z10_LON, params.Z10_NAME, params.Z10_COLOR)
Z11 = Zone(params.Z11_LAT, params.Z11_LON, params.Z11_NAME, params.Z11_COLOR)
Z12 = Zone(params.Z12_LAT, params.Z12_LON, params.Z12_NAME, params.Z12_COLOR)
all_zones = [Z1, Z2, Z3, Z4, Z5, Z6, Z7, Z8, Z9, Z10, Z11, Z12]

def create_paths_to_downtown(DowntownZone: Zone, all_zones: List[Zone], weight: float) -> List[TransitPath]:
    return [TransitPath(DowntownZone, z, weight) for z in all_zones]

def full_connect_zones(zone_group: List[Zone], weight: float) -> List[TransitPath]:
    paths = []
    for index1, z1 in enumerate(zone_group):
        for z2 in zone_group[index1:]:
            new_path = TransitPath(z1, z2, weight)
            paths.append(new_path)

    return paths

class ZoneEvaluator:
    
    zones = all_zones
    zone_paths = [p for p in create_paths_to_downtown(Z2, all_zones, 1.0)] + \
        [p for p in full_connect_zones([z for z in all_zones if z != Z2], 0.5)]

    # zone_paths = [(Z1, Z2, 1.0), 
    #               (Z3, Z2, 1.0), 
    #               (Z4, Z2, 1.0),
    #               (Z5, Z2, 1.0), 
    #               (Z6, Z2, 1.0), 
    #               (Z7, Z2, 1.0), 
    #               (Z8, Z2, 1.0),
    #               (Z9, Z2, 1.0), 
    #               (Z1, Z3, 0.5),
    #               ()]

    def __init__(self, initial_network: TransitNetwork):
        self.initial_network = initial_network
        self.pool_of_stops = initial_network.stops 
        self.zone_keys = dict([(z, i) for i, z in enumerate(self.zones)])
        self.stops_in_zone = [self.determine_stops_in_range(z) for z in self.zones]
        self.current_stop_choices = {}
        self.initial_zone_score = 0

        self.sample_stops()
        self.log_choices()
        
    def log_choices(self) -> None:

        result_str = '*\n'
        for zone in self.zones:
            result_str += str(zone)
            for stop_choice in self.current_stop_choices[self.get_zone_key(zone)]:
                result_str += '\t'
                result_str += str(stop_choice)
                result_str += '\n'

        RootLogger.log_info(result_str)

    def get_zone_key(self, zone: Zone) -> int:
        return self.zone_keys[zone]
    
    def get_zone_stops(self, zone: Zone) -> List[Stop]:
        zone_key = self.get_zone_key(zone)
        return self.stops_in_zone[zone_key]
    
    def determine_stops_in_range(self, zone: Zone) -> List[str]:
        stops = [s.id for s in self.pool_of_stops if s.distance_to_point(zone) < params.ZONE_RADIUS]
        if stops == []:
            RootLogger.log_error(f'Failed to find stops within range {params.ZONE_RADIUS} of {zone.get_coords()}')
        else:
            RootLogger.log_info(f'Found {len(stops)} stops within range {params.ZONE_RADIUS} of {zone.get_coords()}')
        return stops
    
    def sample_stop_for_zone(self, zone: Zone): 
        stop_options = self.get_zone_stops(zone)
        # TODO: Could sample here by population weight, or by ridership weight. 
        stop_choice = random.choice(stop_options)
        return stop_choice
    
    def sample_stops(self):
        for z in self.zones:
            z_key = self.get_zone_key(z) 
            self.current_stop_choices[z_key] = [self.sample_stop_for_zone(z) for i in range(params.ZONE_SAMPLE_NUM)]
        # Update initial_zone_score with new sample
        self.initial_zone_score = self.evaluate_total_zone_distance(self.initial_network)
    
    def trip_distance_to_zone(self, trip: SimpleTrip, stop_index: int, target_zone: Zone) -> int:
        trip_length = len(trip.stops)
        cur_index_inc = stop_index
        cur_index_dec = stop_index
        target_stops = self.get_zone_stops(target_zone)
        # Basically a BFS on a list. Find nearest stop in that group by branching out left and right. 
        distance = 0 
        while cur_index_inc < trip_length or cur_index_dec >= 0:
            if cur_index_inc < trip_length and trip.stops[cur_index_inc].id in target_stops:
                return distance
            
            if cur_index_dec >= 0 and trip.stops[cur_index_dec].id in target_stops:
                return distance
            
            cur_index_inc += 1
            cur_index_dec -= 1

            distance += 1
        
        return float('inf')

    def route_distance_to_zone(self, route: SimpleRoute, source_stop: Stop, target_zone: Zone) -> int:
        trip_distances = []
        for trip in route.trips:
            if trip.does_stop_at(source_stop):
                stop_index = trip.get_index_of_stop_id(source_stop)
                trip_distances.append(self.trip_distance_to_zone(trip, stop_index, target_zone))
        
        if trip_distances == []:
            error_msg = f'Neither trip of route {route.id} contained stop {source_stop} that claimed to have route {route.id}!'
            RootLogger.log_error(error_msg)
            raise ValueError(error_msg)

        return min(trip_distances)

    def evaluate_zone_distance(self, target_network: TransitNetwork, source_zone: Zone, target_zone: Zone) -> float:
        source_zone_key = self.get_zone_key(source_zone)
        all_source_stops = self.current_stop_choices[source_zone_key]
        routes_dist = []
        all_route_options = []

        # Look at all stops sampled. 
        for source_stop in all_source_stops:

            # If the stop got removed at some point, just skip it in calculations
            if not target_network.has_stop(source_stop):
                continue 
            
            route_options = target_network.get_stop_transfers(source_stop)
            all_route_options += route_options

            # Error cases
            if route_options == [] and target_network.has_stop(source_stop):
                stop_route_id, stop_trip_id = target_network.search_for_stop(source_stop)
                RootLogger.log_error(f'Found stop {source_stop.id} with no routes in network {target_network.id}!')
                if stop_route_id != None and stop_trip_id != None:
                    RootLogger.log_error(f'Network contained stop on route {stop_route_id} and trip {stop_trip_id}, but has no transfers.')
            
            # Compute Distance
            for route_id in route_options:
                route = target_network.lookup_route_by_id(route_id)
                try:
                    route_dist = self.route_distance_to_zone(route, source_stop, target_zone)
                except ValueError:
                    error_msg = f'Stops of network {target_network.id} are improperly updated.'
                    RootLogger.log_error(error_msg)
                    raise TypeError(error_msg)

                routes_dist.append(route_dist)

        if routes_dist == [] or min(routes_dist) == float('inf'):
            RootLogger.log_warning(f'Unable to find route from {source_zone} to {target_zone}, giving distance of {params.DEFAULT_ZONE_DISTANCE}')
            RootLogger.log_warning(f'None of {all_route_options} reach {target_zone}!')
            return params.DEFAULT_ZONE_DISTANCE

        return min(routes_dist)

    def evaluate_total_zone_distance(self, target_network: TransitNetwork):
        total_zone_distance = 0.0

        for path in self.zone_paths:
            source_zone, target_zone, weight = path.to_tuple()

            dist_1 = self.evaluate_zone_distance(target_network, source_zone, target_zone)
            dist_2 = self.evaluate_zone_distance(target_network, target_zone, source_zone)
            total_zone_distance += ((dist_1 + dist_2) / 2.0)*weight

        return total_zone_distance
    
    def evaluate_network(self, target_network: TransitNetwork):
        raw_zone_dist = self.evaluate_total_zone_distance(target_network)
        if raw_zone_dist == 0:
            RootLogger.log_warning(f'Initial network achieved score of 0, setting to {params.ZONE_EPSILON}.')
            zone_score = (self.initial_zone_score) / (params.ZONE_EPSILON)
        else:
            zone_score = (self.initial_zone_score) / raw_zone_dist
        return zone_score
                

            
    
    

    
    
        

