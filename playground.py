from preprocessing.ridership_data import RidershipData, RawRidershipData
from preprocessing.gtfs_data import GTFSData
from transit_network.transit_network import create_network_from_GTFSRoutes
"""
This script is purely for informal testing and 'playing' with new code. 
"""

RRD = RawRidershipData('data/ridership_data/SFMTA.xlsx', 'SF')
RD = RidershipData(RRD)
RD.export_data()

SF_GTFS = GTFSData('data/gtfs_data/SFMTA.zip', 'SF')
matched_routes = RD.get_matched_ids_from_gtfs(SF_GTFS)
SF_GTFS.set_trips_for_all_routes(matched_routes)

result = create_network_from_GTFSRoutes(matched_routes)
print(result)
# Next step is to trim the shapes associated with each route. 

# first_trip = trips_from_routes['1'][0]
# stops_from_trip = SF_GTFS.get_stops_for_trip_id(first_trip)
# Want to sub parent station for station id when possible. 