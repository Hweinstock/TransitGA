import pandas as pd  
import pathlib 

class RidershipData():

    def read_data(self):
        df = pd.read_excel(self.filepath)
        return df 

if __name__ == '__main__':
    RD = RidershipData('data/ridership_data/SFMTA.xlsx')
    print(RD.read_data())