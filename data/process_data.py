import streamlit as st
from datetime import datetime

def process_data(df, data_desejada, numero_instalacao):
    """
    Filtra o dataframe de acordo com a data desejada e as modalidades escolhidas.
    
    Parâmetros:
    - df: dataframe com os dados
    - data_desejada: data desejada para filtro (datetime ou string no formato 'mm/aaaa')
    - numero_instalacao: lista de modalidades desejadas
    
    Retorna:
    - df_filtered: dataframe filtrado
    - mes_periodo: período da data desejada
    """
    
    # Converte a data desejada para datetime se estiver em string
    # Obs: o formato de entrada é 'mm/aaaa'
    data_desejada = datetime.strptime(data_desejada, '%m/%Y') if isinstance(data_desejada, str) else data_desejada
    
    # Formata a data desejada para o formato 'mm/aaaa'
    mes_periodo = data_desejada.strftime('%m/%Y')
    
    # Filtra o dataframe por período e modalidade
    # Obs: a coluna 'Período' deve ter o formato 'mm/aaaa'
    df_filtered = df[(df['Período'] == mes_periodo) & (df['Modalidade'].isin(numero_instalacao))]
    
    # Exibe dados filtrados para depuração
    # Obs: usar st.write para exibir dataframe completo
    st.write("Dados filtrados por período e modalidade:", df_filtered)
    
    # Arredonda valores do saldo atual para 2 casas decimais
    df_filtered['Saldo Atual'] = df_filtered['Saldo Atual'].round(2)
    
    # Armazena a data desejada no estado da sessão
    # Obs: o estado da sessão é usado para armazenar variáveis entre chamadas de função
    st.session_state.data_desejada = data_desejada

    return df_filtered, mes_periodo

