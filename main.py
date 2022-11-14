from preprocessing.ridership_data import RidershipData, RawRidershipData

RRD = RawRidershipData('data/ridership_data/SFMTA.xlsx', 'SF')
RD = RidershipData(RRD)
print(RD.read_data())