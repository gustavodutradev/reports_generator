import pandas as pd

class DataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
    
    def read_data(self):
        self.data = pd.read_excel(self.file_path, header=1)
        return self.data
