from preprocessing.ridership_data import RidershipData, RawRidershipData
from preprocessing.gtfs_data import GTFSData
"""
This script is purely for informal testing and 'playing' with new code. 
"""

RRD = RawRidershipData('data/ridership_data/SFMTA.xlsx', 'SF')
RD = RidershipData(RRD)
RD.export_data()

SF_GTFS = GTFSData('data/gtfs_data/SFMTA.zip', 'SF')
matched_routes = RD.get_matched_ids_from_gtfs(SF_GTFS)
trips_from_routes = SF_GTFS.get_trips_for_route(matched_routes)
first_trip = trips_from_routes['1'][0]
stops_from_trip = SF_GTFS.get_stops_for_trip_id(first_trip)
# Want to sub parent station for station id when possible. 
print(stops_from_trip)