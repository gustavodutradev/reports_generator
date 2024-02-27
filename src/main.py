from data_loader import DataLoader
from report_generator import ReportGenerator

def main(file_path, output_folder, template_text):
    try:
        data_reader = DataLoader(file_path)
        data = data_reader.load_dataframe()

        report_generator = ReportGenerator(output_folder, template_text, data)
        report_generator.save_report()

        return True
    except Exception as e:
        print(f"Erro ao criar relatórios: {e}")
        return False
