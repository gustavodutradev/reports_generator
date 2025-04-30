import locale
from datetime import datetime, timedelta
from docx import Document
import pandas as pd

class DataProcessor:
    def __init__(self, data, template_text):
        self.template_text_path = template_text
        self.template_text = self.load_template_text()
        self.data = data

    def get_reference_date(self):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        today = datetime.now()
        first_day = today.replace(day=1)
        previous_month = first_day - timedelta(days=1)
        mes_referencia = previous_month.month
        month_string = previous_month.strftime("%B")

        ano_atual = today.year
        ano_referencia = ano_atual if today.month > 1 else ano_atual - 1

        return month_string, ano_referencia, mes_referencia

    def load_template_text(self):
        doc = Document(self.template_text_path)
        return "\n".join([p.text for p in doc.paragraphs])

    def format_BRL_currency(self, valor):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        return locale.currency(valor, grouping=True) if valor is not None else None

    def generate_customer_report(self, row, nome):
        periodo = self.get_reference_date()[0]
    
        # Extrai valores, aplicando 0 caso seja NaN
        raw_mtd = row.get("profitability_mtd", 0) * 100
        rentabilidade_mes = 0 if pd.isna(raw_mtd) else raw_mtd
    
        raw_cdi_mtd = row.get("cdi_mtd", 0)
        if raw_cdi_mtd == 0 or pd.isna(raw_cdi_mtd):
            performance_cdi_mes = 0
        else:
            performance_cdi_mes = rentabilidade_mes / float(raw_cdi_mtd)
    
        raw_profit_mtd = row.get("profit_mtd", 0)
        balanco_mes = 0 if pd.isna(raw_profit_mtd) else float(raw_profit_mtd)
    
        # Mesmo para 12m
        raw_12m = row.get("profitability_12m", 0) * 100
        rentabilidade_acumulada = 0 if pd.isna(raw_12m) else raw_12m
    
        raw_cdi_12m = row.get("cdi_12m", 0)
        if raw_cdi_12m == 0 or pd.isna(raw_cdi_12m):
            performance_cdi_acum = 0
        else:
            performance_cdi_acum = rentabilidade_acumulada / float(raw_cdi_12m)
    
        raw_profit_12m = row.get("profit_12m", 0)
        balanco_acumulado = 0 if pd.isna(raw_profit_12m) else float(raw_profit_12m)
    
        # Formata tudo sem erros de NaN
        return self.template_text.format(
            nome=nome,
            periodo=periodo,
            rentabilidade_mes=round(rentabilidade_mes, 2),
            performance_cdi_ultimo_mes=round(performance_cdi_mes, 2),
            balanco_mes=self.format_BRL_currency(balanco_mes),
            rentabilidade_acumulada=round(rentabilidade_acumulada, 2),
            performance_cdi_acumulada=round(performance_cdi_acum, 2),
            balanco_acumulado=self.format_BRL_currency(balanco_acumulado),
        )