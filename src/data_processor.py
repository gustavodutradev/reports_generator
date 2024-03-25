import locale
from datetime import datetime, timedelta
from docx import Document
import pandas as pd

class DataProcessor:    
    def __init__(self, data, template_text=None):
        self.template_text = template_text
        self.data = data

    def get_reference_date(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        today = datetime.now()
        first_day = today.replace(day=1)
        previous_month = first_day - timedelta(days=1)
        mes_referencia = previous_month.month
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

        rentabilidade_mes_key = 'Rentabilidade.11'
        rentabilidade_mes = customer_data.get(rentabilidade_mes_key, 0)

        balanco_mes_key = 'Lucro/Prejuízo.11'
        balanco_mes = customer_data.get(balanco_mes_key, 0)

        performance_cdi_ultimo_mes = customer_data.get('Performance X CDI (Último mês)', 0)

        rentabilidade_acumulada = customer_data.get('Rentabilidade.12', 0)
        performance_cdi_acumulada = customer_data.get('Performance X CDI (12 meses)', 0)
        balanco_acumulado = customer_data.get('Lucro/Prejuízo.12', 0)

        nome = str(customer_data.get('Nome', '')).capitalize()
        performance_cdi_ultimo_mes *= 100
        performance_cdi_acumulada *= 100

        balanco_mes = float(balanco_mes) if balanco_mes is not None else 0
        performance_cdi_ultimo_mes = float(performance_cdi_ultimo_mes) if performance_cdi_ultimo_mes is not None else 0
        rentabilidade_acumulada = float(rentabilidade_acumulada) if rentabilidade_acumulada is not None else 0
        performance_cdi_acumulada = float(performance_cdi_acumulada) if performance_cdi_acumulada is not None else 0
        balanco_acumulado = float(balanco_acumulado) if balanco_acumulado is not None else 0

        text = template_text.format(
            nome=nome,
            periodo=periodo,
            rentabilidade_mes=round(float(rentabilidade_mes) * 100, 2),
            performance_cdi_ultimo_mes=round(float(performance_cdi_ultimo_mes)),
            balanco_mes=self.format_BRL_currency(float(balanco_mes)),
            rentabilidade_acumulada=round(float(rentabilidade_acumulada) * 100, 2),
            performance_cdi_acumulada=round(float(performance_cdi_acumulada)),
            balanco_acumulado=self.format_BRL_currency(float(balanco_acumulado))
        )
        return text
