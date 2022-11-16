from preprocessing.ridership_data import RidershipData, RawRidershipData
from preprocessing.gtfs_data import GTFSData
"""
This script is purely for informal testing and 'playing' with new code. 
"""

RRD = RawRidershipData('data/ridership_data/SFMTA.xlsx', 'SF')
RD = RidershipData(RRD)
RD.export_data()

SF_GTFS = GTFSData('data/gtfs_data/SFMTA.zip', 'SF')
print(type(SF_GTFS.read_data()))