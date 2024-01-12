import pandas as pd
import json
from data_processor import DataProcessor

class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def convert_to_json(self):
        print("Caminho do arquivo:", self.file_path)
        if self.file_path.endswith(('.xlsx')):
            data_frame = pd.read_excel(self.file_path, header=1)
        else:
            raise ValueError("Formato de arquivo não suportado. Use CSV ou Excel (xlsx)")

        # Converte o DataFrame para JSON
        json_data = data_frame.to_json(orient='records')

        dict_json = json.loads(json_data)

        return dict_json

    def save_json(self, json_data):
        try:
            with open('data.json', 'w') as file:
                json.dump(json_data, file, indent=4)
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo não encontrado.")

        return True
    

    def run(self):
        json_data = self.convert_to_json()
        self.save_json(json_data)
        return True
