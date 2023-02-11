from preprocessing.ridership_data import RidershipData, RawRidershipData
from preprocessing.gtfs_data import GTFSData
from transit_network.transit_network import create_network_from_GTFSRoutes, TransitNetwork

from utility import pickle_object


def generate_compression_metrics(Gtfs: GTFSData, SimplifiedNetwork: TransitNetwork) -> str:
    original_num_routes = Gtfs.num_routes
    original_num_trips = Gtfs.num_trips
    original_num_stops = Gtfs.num_stops 

    new_num_routes = SimplifiedNetwork.num_routes
    new_num_trips = SimplifiedNetwork.num_trips
    new_num_stops = SimplifiedNetwork.num_stops 

    return f'Reduced number of routes from {original_num_routes} to {new_num_routes}, \n \
             Reduced number of trips from {original_num_trips} to {new_num_trips}, \n \
             Reduced number of stops from {original_num_stops} to {new_num_stops}. '

def create_simplified_gtfs_SFMTA(export_file='initial_network') -> str:
    """Full end-to-end generation of the network from ridership and GTFS data. 

    Args:
        export_name (str, optional):  Defaults to 'initial_network'.

    Returns:
        str: compression metrics report
    """
    RRD = RawRidershipData('data/ridership_data/SFMTA.xlsx', 'SF')
    RD = RidershipData(RRD)
    RD.export_data()

    SF_GTFS = GTFSData('data/gtfs_data/SFMTA.zip', 'SF')

    matched_routes = RD.get_matched_ids_from_gtfs(SF_GTFS)
    SF_GTFS.set_trips_for_all_routes(matched_routes)

    Network = create_network_from_GTFSRoutes(matched_routes, SF_GTFS.read_data().shapes)
    compression_metrics_str = generate_compression_metrics(SF_GTFS, Network)
    pickle_object(Network, export_file)
    Network.write_to_gtfs(export_file)
    return compression_metrics_str