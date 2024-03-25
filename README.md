
# Gerador de Relatórios

Este reposítorio contém código de um gerador de relatórios feito em Python. O gerador utiliza como base uma planilha excel e um arquivo de template onde são inputados os dados da planilha, à serem enviados para clientes.

O gerador implementa a seguinte estrutura de pastas:

Período de referência -> Pasta de cada assessor -> Em cada assessor, os relatórios de seus respectivos clientes.

É gerado um arquivo txt ao final com o feedback do processo, cruzando dados da quantidade de clientes de cada assessor, e quantos relatórios foram gerados. Isto, para determinar alguma divergência ou erro na geração de algum relatório.

## Bibliotecas Python utilizadas

- Pandas
- Numpy
- Flet (GUI)
- Docx
- Datetime
- Locale

## Aprendizados

Tive diversos aprendizados ao criar esta ferramenta, entre eles o estudo sobre empacotamento de aplicações python, aprofundamento e uso da biblioteca Pandas e criação de interfaces gráficas em python com Flet e Tkinter.

Aprendizados sobre threading, manipulação de datas, criação de arquivos e pastas também foram parte importante do processo.

Os erros também ensinaram muito, sobretudo na necessidade de não deixar exceções sem tratamento.

A versão final possui tratamento em todos as etapas do processo, desde a seleção dos arquivos e pastas base, bem como a criação de todos os relatórios por assessor.

Não utilizei TDD, e os testes serão o próximo passo para este código, e será com certeza mais um aprendizado.
