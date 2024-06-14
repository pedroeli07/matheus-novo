import pandas as pd
from datetime import datetime
from image.image import generate_image
from data.formaters import format_value, format_currency


# Função para processar os dados
def process_data(df, data_desejada, numero_instalacao):
    """
    Função para processar os dados de acordo com a data desejada e as instalações selecionadas.
    
    Parâmetros:
    df (pandas.DataFrame): DataFrame com os dados originais
    data_desejada (str ou datetime): Data desejada para filtragem
    numero_instalacao (list): Lista de instalações selecionadas
    
    Retorna:
    tuple: Duas variáveis: df_filtered, mes_periodo
        - df_filtered (pandas.DataFrame): DataFrame filtrado com os dados da data desejada e das instalações selecionadas
        - mes_periodo (str): Representação da data desejada no formato 'mm/aaaa'
    """
    # Converter a data desejada para objeto datetime se ainda não estiver
    if isinstance(data_desejada, str):
        data_desejada = datetime.strptime(data_desejada, '%m/%Y')
    # Criar uma representação da data desejada no formato 'mm/aaaa'
    mes_periodo = data_desejada.strftime('%m/%Y')
    # Filtrar o DataFrame de acordo com a data desejada e as instalações selecionadas
    df_filtered = df[(df['Período'] == mes_periodo) & (df['Modalidade'].isin(numero_instalacao))]
    # Arredondar os valores da coluna 'Saldo Atual' para duas casas decimais
    df_filtered['Saldo Atual'] = df_filtered['Saldo Atual'].round(2)
    # Retornar o DataFrame filtrado e a representação da data desejada
    return df_filtered, mes_periodo


# Função para preparar o DataFrame
def prepare_dataframe(df_filtered2, VALOR_KWH_FATURADO, calculo_tipo):
    """
    Função para preparar o DataFrame de acordo com o tipo de cálculo selecionado.
    
    Parâmetros:
    df_filtered2 (pandas.DataFrame): DataFrame filtrado com os dados da data desejada e das instalações selecionadas
    VALOR_KWH_FATURADO (float): Valor do kWh faturado
    calculo_tipo (str): Tipo de cálculo selecionado ('Recebimento' ou 'Compensação')
    
    Retorna:
    pandas.DataFrame: DataFrame preparado com as colunas renomeadas e os valores calculados
    """
    # Criar uma cópia do DataFrame filtrado
    preprocessed_df = df_filtered2.copy()

    # Remover as colunas 'Transferido' e 'Geração'
    preprocessed_df.drop(['Transferido', 'Geração'], axis=1, inplace=True)

    # Filtrar linhas onde a coluna 'Modalidade' não é igual a 'Auto Consumo-Geradora'
    preprocessed_df = preprocessed_df.query("Modalidade != 'Auto Consumo-Geradora'")

    # Arredondar os valores de todas as colunas numéricas para duas casas decimais
    preprocessed_df = preprocessed_df.round(2)

    # Calcular o valor da coluna 'Valor (R$)', com base na coluna selecionada pelo usuário e no valor do kWh faturado
    if calculo_tipo == 'Recebimento':
        preprocessed_df['Valor (R$)'] = preprocessed_df['Recebimento'] * VALOR_KWH_FATURADO
    else:
        preprocessed_df['Valor (R$)'] = preprocessed_df['Compensação'] * VALOR_KWH_FATURADO

    # Renomear a coluna 'Modalidade' para 'Referência'
    preprocessed_df.rename(columns={'Modalidade': 'Referência'}, inplace=True)

    # Excluir linhas onde os valores nas colunas 'Compensação' e 'Recebimento' são iguais a zero
    preprocessed_df = preprocessed_df[(preprocessed_df['Compensação'] != 0) & (preprocessed_df['Recebimento'] != 0)]

    # Retornar o DataFrame preparado
    return preprocessed_df

# Função para adicionar uma linha total ao DataFrame
def add_total_row(preprocessed_df_filtered):
    """
    Função para adicionar uma linha total ao DataFrame.
    
    Parâmetros:
    preprocessed_df_filtered (pandas.DataFrame): DataFrame preparado com as colunas renomeadas e os valores calculados
    
    Retorna:
    pandas.DataFrame: DataFrame com a linha total adicionada e os valores formatados
    """
    # Calcular a soma dos valores numéricos do DataFrame
    total_row = preprocessed_df_filtered.sum(numeric_only=True)
    # Adicionar a coluna 'Referência' com o valor 'Total'
    total_row['Referência'] = 'Total'
    
    # Caso a coluna 'Valor (R$)' esteja presente no DataFrame
    if 'Valor (R$)' in preprocessed_df_filtered.columns:
        # Calcular a soma dos valores da coluna 'Valor (R$)'
        total_row['Valor (R$)'] = preprocessed_df_filtered['Valor (R$)'].sum()
        # Formatá-lo como moeda
        total_row['Valor (R$)'] = format_currency(total_row['Valor (R$)'])
    
    # Para cada coluna do tipo objeto no DataFrame
    for col in preprocessed_df_filtered.select_dtypes(include=['object']).columns:
        # Se a coluna não for 'Referência'
        if col != 'Referência':
            # Colocar um valor vazio naquela coluna na linha total
            total_row[col] = ''
    
    # Concatenar a linha total ao DataFrame
    preprocessed_df_filtered = pd.concat([preprocessed_df_filtered, pd.DataFrame(total_row).T], ignore_index=True)
    
    # Caso a coluna 'Valor (R$)' esteja presente no DataFrame
    if 'Valor (R$)' in preprocessed_df_filtered.columns:
        # Formatá-lo como moeda para cada valor da coluna 'Valor (R$)'
        preprocessed_df_filtered['Valor (R$)'] = preprocessed_df_filtered['Valor (R$)'].apply(lambda x: format_currency(x) if isinstance(x, (int, float)) else x)
    
    # Retornar o DataFrame com a linha total adicionada
    return preprocessed_df_filtered



