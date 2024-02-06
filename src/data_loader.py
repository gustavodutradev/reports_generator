import pandas as pd

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
        
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo não encontrado.")

        return self.data

