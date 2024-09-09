import pytest
import pandas as pd
import numpy as np
import os
from src.data_loader import DataLoader

@pytest.fixture
def sample_excel_file():
    # Criar um arquivo Excel temporário com pandas
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, np.nan],
        'C': [7, 8, 9]
    })
    file_path = 'test_file.xlsx'
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=1)
    yield file_path
    # Limpar o arquivo após o teste
    os.remove(file_path)

def test_load_dataframe_valid_excel(sample_excel_file):
    loader = DataLoader(sample_excel_file)
    df = loader.load_dataframe()

    # Verifique se o DataFrame foi carregado corretamente
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 3)  # Ajuste a forma esperada conforme o DataFrame criado
    assert df.isnull().sum().sum() == 0  # Verifique se não há valores NaN

def test_load_dataframe_invalid_format():
    loader = DataLoader('test_file.txt')  # Arquivo com formato não suportado
    with pytest.raises(ValueError) as excinfo:
        loader.load_dataframe()
    assert str(excinfo.value) == "Formato de arquivo não suportado. Use CSV ou Excel (xlsx)"

def test_load_dataframe_file_not_found():
    loader = DataLoader('non_existent_file.xlsx')
    with pytest.raises(FileNotFoundError) as excinfo:
        loader.load_dataframe()
    assert str(excinfo.value) == "Arquivo não encontrado."
