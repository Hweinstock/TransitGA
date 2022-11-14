from preprocessing.ridership_data import RidershipData, RawRidershipData

"""
This script is purely for informal testing and 'playing' with new code. 
"""

RRD = RawRidershipData('data/ridership_data/SFMTA.xlsx', 'SF')
RD = RidershipData(RRD)
RD.export_data()