import pandas as pd
import streamlit as st
from datetime import datetime

# Inicializa o estado da sessão se ainda não definido
if 'data_desejada' not in st.session_state or 'modalidade' not in st.session_state:
    # Define uma data padrão
    st.session_state.data_desejada = datetime(2000, 1, 1) 
    # Define uma lista vazia para armazenar as modalidades
    st.session_state.modalidade = [] 


def load_data():
    """
    Carrega dados de um arquivo CSV ou XLSX para um DataFrame pandas.

    Retorna:
        DataFrame pandas: O DataFrame carregado com os dados do arquivo.
    """

    # Opção para carregar arquivos CSV ou XLSX
    uploaded_file = st.file_uploader(
        "Escolha o arquivo CSV ou XLSX",  # Mensagem exibida ao usuário
        type=["csv", "xlsx"]  # Tipos de arquivos permitidos
    )

    # Carrega o arquivo baseado no tipo
    if uploaded_file is not None:
        if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(uploaded_file)  # Carrega um arquivo XLSX
        else:
            df = pd.read_csv(
                uploaded_file,
                delimiter=";",  # Delimitador de colunas
                decimal=",",  # Separador decimal
                encoding="latin1",  # Codificação do arquivo
                dtype={"Instalação": str}  # Dicionário para definir o tipo de dados das colunas
            )  # Carrega um arquivo CSV

        # Limpeza e ajuste na coluna de instalação
        df['Instalação'] = df['Instalação'].astype(str).str.replace(',', '')  # Remove vírgulas da coluna 'Instalação'

        # Mapeamento de modalidades por número de instalação
        # Dicionário com os números de instalação e suas respectivas modalidades
        modalidade_map = {
            "3013110767": "GBBH - Lj 02",
            "3013096188": "GBBH - Lj 01",
            "3004402254": "Bebedouro",
            "3011883117": "Porks Savassi",
            "3014657899": "Porks Castelo"
        }

        # Atualiza a coluna 'Modalidade' com as modalidades correspondentes
        for index, row in df.iterrows():
            instalacao = row['Instalação']
            modalidade = modalidade_map.get(instalacao)  # Retorna o valor do dicionário ou None se não for encontrado
            if modalidade is not None:  # Verifica se o valor foi encontrado no dicionário
                df.loc[index, 'Modalidade'] = modalidade

        # Exibe o DataFrame no Streamlit
        st.write(df)

        # Colunas a serem removidas
        cols_to_drop = [
            "Quantidade Saldo a Expirar",
            "Período Saldo a Expirar",
            "Quota",
            "Posto Horário",
            "Saldo Anterior",
            "Saldo Expirado"
        ]
        df = df.drop(columns=cols_to_drop)

        return df
    else:
        return pd.DataFrame()  # Retorna um DataFrame vazio se nenhum arquivo for carregado



