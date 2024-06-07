import pandas as pd
import os

def clean_data(file_path):
    # Verifique se o arquivo existe
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Carregar os dados
    df = pd.read_csv(file_path, low_memory=False)
    
    # Converter a coluna 'Date' para datetime com formato especificado
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y', errors='coerce')
    
    # Remover duplicatas
    df.drop_duplicates(inplace=True)
    
    # Remover registros com valores nulos
    df.dropna(inplace=True)
    
    # Adicionar coluna de valor total
    df['TotalPrice'] = df['Qty'] * df['Amount']
    
    return df

if __name__ == "__main__":
    # Usar caminho absoluto para o arquivo
    file_path = os.path.abspath(os.path.join('data', 'Amazon_Sale_Report.csv'))
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    cleaned_df = clean_data(file_path)
    cleaned_df.to_csv(os.path.abspath(os.path.join('data', 'cleaned_Amazon_Sale_Report.csv')), index=False)
    print("Data cleaning completed and file saved.")
