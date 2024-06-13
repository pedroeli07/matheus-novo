import pandas as pd

def ordenar_periodo(mes_data, coluna='Período'):
    """
    Ordena os dados de acordo com a coluna 'Período' no formato 'Mês/Ano'.
    Os meses são convertidos para inglês antes da ordenação e revertidos para português após.

    Parâmetros:
    - mes_data (DataFrame): DataFrame contendo os dados a serem ordenados.
    - coluna (str): Nome da coluna a ser ordenada. Padrão: 'Período'.

    Retorna:
    - DataFrame: DataFrame com os dados ordenados.
    """

    # Mapeamento dos meses de português para inglês
    month_mapping_pt_to_en = {
        "Jan": "Jan",
        "Fev": "Feb",
        "Mar": "Mar",
        "Abr": "Apr",
        "Mai": "May",
        "Jun": "Jun",
        "Jul": "Jul",
        "Ago": "Aug",
        "Set": "Sep",
        "Out": "Oct",
        "Nov": "Nov",
        "Dez": "Dec"
    }

    # Mapeamento dos meses de inglês para português
    month_mapping_en_to_pt = {v: k for k, v in month_mapping_pt_to_en.items()}

    # Separar a linha de média dos outros dados
    non_average = mes_data[mes_data[coluna] != 'Média']
    average = mes_data[mes_data[coluna] == 'Média']

    # Converter os nomes dos meses de português para inglês para ordenação
    non_average[coluna] = non_average[coluna].apply(lambda x: x.replace(x[:3], month_mapping_pt_to_en[x[:3]]))
    non_average[coluna] = pd.to_datetime(non_average[coluna], format='%b/%Y')
    non_average = non_average.sort_values(by=coluna).reset_index(drop=True)

    # Reverter os nomes dos meses de inglês para português para exibição
    non_average[coluna] = non_average[coluna].dt.strftime('%b/%Y')
    non_average[coluna] = non_average[coluna].apply(lambda x: x.replace(x[:3], month_mapping_en_to_pt[x[:3]]))

    # Combinar os dados de volta, incluindo a linha de média
    sorted_data = pd.concat([non_average, average]).reset_index(drop=True)

    return sorted_data

