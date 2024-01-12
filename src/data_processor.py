import locale
from datetime import datetime, timedelta
from docx import Document

class DataProcessor:    
    def __init__(self, data, template_text=None):
        self.template_text = template_text
        self.data = data
    
    def get_reference_date(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        today = datetime.now()
        first_day = today.replace(day=1)
        previous_month = first_day - timedelta(days=1)
        month_string = previous_month.strftime('%B')

        ano_atual = today.year
        mes_atual = today.month

        if mes_atual == 1:
            mes_referencia = 12
            ano_referencia = ano_atual - 1
        else:
            ano_referencia = ano_atual

        return month_string, ano_referencia, mes_referencia
    
    def load_template_text(self):
        try:
            doc_path = self.template_text
            doc = Document(doc_path)

            text = "\n".join([para.text for para in doc.paragraphs])

            return text
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo não encontrado.")
        
    def format_BRL_currency(self, valor):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(valor, grouping=True) if valor is not None else None
    
    def generate_customer_report(self, customer_data):
        template_text = self.load_template_text()

        periodo = self.get_reference_date()[0]
        reference_month_number = self.get_reference_date()[2]

        if reference_month_number == 1:
            rentabilidade_mes = float(customer_data['Rentabilidade']) if customer_data['Rentabilidade'] is not None else None
            balanco_mes = self.format_BRL_currency(float(customer_data['Lucro/Prejuízo'])) if customer_data['Lucro/Prejuízo'] is not None else None
        else:
            rentabilidade_mes = float(customer_data[f'Rentabilidade.{reference_month_number - 1}'] * 100) if customer_data[f'Rentabilidade.{reference_month_number - 1}'] is not None else None
            balanco_mes = self.format_BRL_currency(customer_data[f'Lucro/Prejuízo.{reference_month_number - 1}'])
        
        nome = customer_data['Nome'].capitalize()
        performance_cdi_ultimo_mes = float(customer_data['Performance X CDI (Último mês)'] * 100) if customer_data['Performance X CDI (Último mês)'] is not None else None
        
        rentabilidade_acumulada = float(customer_data['Rentabilidade.12'] * 100) if customer_data['Rentabilidade.12'] is not None else None
        performance_cdi_acumulada = float(customer_data['Performance X CDI (12 meses)'] * 100) if customer_data['Performance X CDI (12 meses)'] is not None else None
        balanco_acumulado = self.format_BRL_currency(customer_data['Lucro/Prejuízo.12']) if customer_data['Lucro/Prejuízo.12'] is not None else None

        text = template_text.format(
            nome=nome,
            periodo=periodo,
            rentabilidade_mes=round(rentabilidade_mes, 2),
            performance_cdi_ultimo_mes = round(performance_cdi_ultimo_mes, 2),
            balanco_mes=balanco_mes,
            rentabilidade_acumulada=round(rentabilidade_acumulada, 2),
            performance_cdi_acumulada=round(performance_cdi_acumulada, 2),
            balanco_acumulado=balanco_acumulado
        )
        return text
