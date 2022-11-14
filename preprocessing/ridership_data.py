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

    def read_data(self):
        raw_df = self.raw_data.read_data()
        
        return raw_data