import pandas as pd  
from preprocessing.data import DataBase

class RawRidershipData(DataBase):

    def read_data(self) -> pd.DataFrame:
        df = pd.read_excel(self.filepath)
        return df 

class RidershipData(DataBase):

    def __init__(self, raw_data : RawRidershipData):
        self.raw_data = raw_data
        DataBase.__init__(self, raw_data.filepath, raw_data.city_name)

    def read_data(self) -> pd.DataFrame:
        raw_df = self.raw_data.read_data()
        routes = raw_df['Route']
        total_ridership_data = []

        # Total up ridership for each route
        for route in set(routes):
            
            # Double dash ids exist. Currently we remove dashes and mash together
            route_lst = route.split('-')
            route_id = "".join(route_lst[:-1])
            route_name = route_lst[-1]
            subset_df = raw_df.loc[routes == route]

            # We round this value since excel data in SFMTA stores excessive decimal points. 
            total_ridership = int(subset_df['Average Daily Ridership'].sum())
            
            total_ridership_data.append((route_id, route_name, total_ridership))
        new_data = pd.DataFrame(total_ridership_data, 
                    columns=['route_id', 'route_name', 'total_ridership'])
                    
        return new_data