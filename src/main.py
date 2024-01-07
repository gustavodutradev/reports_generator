from data_reader import DataReader
from report_generator import ReportGenerator
import time

def main():

    file_path = "C:\\Users\\gusta\\OneDrive\\Área de Trabalho\\dados.xlsx"
    output_folder = "C:\\Users\\gusta\\OneDrive\\Área de Trabalho\\relatorios"
    template_text = input("Digite o caminho completo para o template: ")
    # template_text = "C:\\Users\\gusta\\OneDrive\\Documentos\\template.docx"
    
    start_time = time.time()
    data_reader = DataReader(file_path)
    data = data_reader.read_data()

    report_generator = ReportGenerator(output_folder, template_text, data)
    report_generator.save_report()

    print(f"Tempo de execução: {round(time.time() - start_time, 3)} segundos.")

    input("Pressione ENTER para sair.")

if __name__ == '__main__':
    main()