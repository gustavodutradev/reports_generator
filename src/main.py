from data_reader import DataReader
from report_generator import ReportGenerator
import sys
import time

def main(file_path, output_folder, template_text):
    start_time = time.time()
    
    data_reader = DataReader(file_path)
    data = data_reader.read_data()

    report_generator = ReportGenerator(output_folder, template_text, data)
    report_generator.save_report()

    print(f"Tempo de execução: {round(time.time() - start_time, 3)} segundos.")

if __name__ == '__main__':
    try:
        output_folder = sys.argv[1]
        template_text = sys.argv[2]
        file_path = sys.argv[3]
        main(file_path, output_folder, template_text)
    except IndexError:
        print("Argumentos inválidos")
