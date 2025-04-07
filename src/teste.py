from src.local_test_runner import main_teste_local

csv_path = "data/Rentabilidade Mensal Por Carteira.csv"
template_path = "data/template.docx"
output_folder = "output_test"

main_teste_local(csv_path, template_path, output_folder)
