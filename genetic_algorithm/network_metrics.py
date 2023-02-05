from typing import Tuple

from root_logger import RootLogger
from transit_network.transit_network import TransitNetwork 

class NetworkMetrics:
    def __init__(self, network: TransitNetwork):
        # self.network = network
        self.network_id = network.id
        self.route_ids = [r.id for r in network.routes]
        self.trip_ids = [t.id for t in network.trips]
        self.stop_ids = [s.id for s in network.stops]
        self.ridership = network.ridership 

        self.num_routes = len(self.route_ids)
        self.coverage = network.coverage
        self.ridership_density_score = network.ridership_density_score
    
    def similarity(self, other) -> Tuple[float, float, float]:
        if self.network_id == other.network_id:
            RootLogger.log_warning('Comparing Networks with identical ids.')

        routes_similarity = (len(set(self.route_ids) & set(other.route_ids)) * 2.0) / (len(self.route_ids) + len(other.route_ids))
        trips_similarity = (len(set(self.trip_ids) & set(other.trip_ids)) * 2.0) / (len(self.trip_ids) + len(other.trip_ids))
        stops_similarity = (len(set(self.stop_ids) & set(other.stop_ids)) * 2.0) / (len(self.stop_ids) + len(other.stop_ids))

        return routes_similarity, trips_similarity, stops_similarity