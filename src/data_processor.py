import locale
from datetime import datetime, timedelta

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
            with open(self.template_text, 'r') as file:
                template = file.read()
        except: 
            raise FileNotFoundError
        return template
    
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
