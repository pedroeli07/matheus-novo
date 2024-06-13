def format_value(val):
    """Formata um valor como float com 2 casas decimais."""
    try:
        val = float(val)
        if val.is_integer():
            return int(val)
        return f'{val:.2f}'
    except (ValueError, TypeError):
        return val


def calculate_consumption_generation(df_copy, calc_type="Geração"):
    """
    Calcula o consumo mensal e a geração/compensação mensal 
    do DataFrame fornecido.

    Parâmetros:
    - df_copy (DataFrame): DataFrame com os dados a serem processados.
    - calc_type (str): Tipo de cálculo a ser realizado. Opções: 'Geração' ou 'Compensação'.
                       Padrão: 'Geração'.

    Retorna:
    - monthly_data (DataFrame): DataFrame com o consumo e a geração/compensação mensais.
    """

    # Define as funções de agregação e renomeiação de colunas
    if calc_type == "Geração":
        aggregation = {
            'Consumo': 'sum', 
            'Geração': lambda x: x[x != 0].sum()
        }
        columns_rename = {
            'Consumo': 'Consumo [kWh]', 
            'Geração': 'Energia Injetada [kWh]'
        }
    elif calc_type == "Compensação":
        aggregation = {
            'Consumo': 'sum', 
            'Compensação': 'sum'
        }
        columns_rename = {
            'Consumo': 'Consumo [kWh]', 
            'Compensação': 'Compensação [kWh]'
        }
    
    # Agrupa os dados mensais somando os consumos e 
    # somente as gerações/compensações não nulas
    monthly_data = df_copy.groupby('Período').agg(aggregation)
    
    # Mapeia os números dos meses para abreviações em português
    months_map = {
        '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr', 
        '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago', 
        '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
    }
    
    # Renomeia os índices para formato de mês abreviado/ano
    monthly_data.index = monthly_data.index.map(
        lambda x: f"{months_map[x.split('/')[0]]}/{x.split('/')[1]}"
    )
    
    # Renomeia as colunas para inclusão das unidades
    monthly_data = monthly_data.rename(columns=columns_rename)
    
    # Calcula a média do consumo e geração/compensação
    average_consumption = monthly_data['Consumo [kWh]'].astype(float).mean()
    if calc_type == "Geração":
        average_generation = monthly_data['Energia Injetada [kWh]'].astype(float).mean()
        monthly_data.loc['Média'] = [average_consumption, average_generation]
    elif calc_type == "Compensação":
        average_compensacao = monthly_data['Compensação [kWh]'].astype(float).mean()
        monthly_data.loc['Média'] = [average_consumption, average_compensacao]
    
    # Arredonda os valores para uma casa decimal e formata os valores
    monthly_data = monthly_data.applymap(format_value)
    
    # Reseta o índice para transformar os períodos em uma coluna novamente
    monthly_data.reset_index(inplace=True)

    return monthly_data

