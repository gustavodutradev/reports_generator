import pandas as pd

class DataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
    
    def read_data(self):
        try:
            self.data = pd.read_excel(self.file_path, header=1)

        except FileNotFoundError:
            raise FileNotFoundError("Arquivo não encontrado. Verifique o caminho e tente novamente. (Não se esqueça do nome do arquivo com a extensão (.csv ou .xlsx) ao final)")
        
        return self.data
