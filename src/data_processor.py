import locale
from datetime import datetime, timedelta
from docx import Document


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

        rentabilidade_mes = float(row.get("profitability_mtd", 0)) * 100
        performance_cdi_ultimo_mes = (
            rentabilidade_mes / float(row.get("cdi_mtd", 1)) if row.get("cdi_mtd", 1) else 0
        )
        balanco_mes = float(row.get("profit_mtd", 0))

        rentabilidade_acumulada = float(row.get("profitability_12m", 0)) * 100
        performance_cdi_acumulada = (
            rentabilidade_acumulada / float(row.get("cdi_12m", 1)) if row.get("cdi_12m", 1) else 0
        )
        balanco_acumulado = float(row.get("profit_12m", 0))

        return self.template_text.format(
            nome=nome,
            periodo=periodo,
            rentabilidade_mes=round(rentabilidade_mes, 2),
            performance_cdi_ultimo_mes=round(performance_cdi_ultimo_mes),
            balanco_mes=self.format_BRL_currency(balanco_mes),
            rentabilidade_acumulada=round(rentabilidade_acumulada, 2),
            performance_cdi_acumulada=round(performance_cdi_acumulada),
            balanco_acumulado=self.format_BRL_currency(balanco_acumulado),
        )
