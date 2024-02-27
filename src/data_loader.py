import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_dataframe(self):
        try:
            if self.file_path.endswith(('.xlsx')):
                self.data = pd.read_excel(self.file_path, header=1)
            else:
                raise ValueError("Formato de arquivo não suportado. Use CSV ou Excel (xlsx)")
            
            self.data = self.data.replace([np.nan], 0)
        
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo não encontrado.")

        return self.data

