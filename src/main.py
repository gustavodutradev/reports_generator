from convert_json import DataHandler
from report_generator import ReportGenerator
import time

def main(file_path, output_folder, template_text):
    start_time = time.time()
    
    data_reader = DataHandler(file_path)
    data = data_reader.convert_to_json()

    report_generator = ReportGenerator(output_folder, template_text, data)
    report_generator.save_report()

    print(f"Tempo de execução: {round(time.time() - start_time, 3)} segundos.")
