from data_reader import DataReader
from report_generator import ReportGenerator

def main():
    file_path = "C:\\Users\\gusta\\OneDrive\\Área de Trabalho\\dados.xlsx"
    output_folder = "C:\\Users\\gusta\\OneDrive\\Área de Trabalho\\relatorios"
    template_text = input("Digite o caminho completo para o template: ")
    
    data_reader = DataReader(file_path)
    data = data_reader.read_data()

    report_generator = ReportGenerator(output_folder, template_text, data)
    report_generator.save_report()

if __name__ == '__main__':
    main()