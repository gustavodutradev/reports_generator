import locale
from datetime import datetime, timedelta
from docx import Document

class DataProcessor:    
    def __init__(self, data, template_text):
        self.template_text = template_text
        self.data = data
    
    def get_previous_month(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        today = datetime.now()
        first_day = today.replace(day=1)
        previous_month = first_day - timedelta(days=1)
        month_string = previous_month.strftime('%B')
        return month_string.capitalize()
    
    def load_template_text(self):
        try:
            doc_path = self.template_text  # Supondo que self.template_text seja o caminho para o arquivo .docx
            doc = Document(doc_path)

            text = "\n".join([para.text for para in doc.paragraphs])

            return text
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo não encontrado.")
    
    def generate_customer_report(self, customer_data):
        template_text = self.load_template_text()
        periodo = self.get_previous_month()
        nome = str(customer_data['Nome']).capitalize()
        rentabilidade_mes = round((customer_data['Rentabilidade mês']), 2)
        cdi = round((customer_data['% CDI']), 2)
        balanco = round((customer_data['Lucro/Prejuízo']), 2)

        text = template_text.format(
            nome=nome,
            periodo=periodo,
            rentabilidade_mes=rentabilidade_mes,
            cdi=cdi,
            balanco=balanco
        )
        return text
