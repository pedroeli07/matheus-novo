import pandas as pd
from PIL import Image
from io import BytesIO
import streamlit as st
from datetime import datetime, timedelta
from data.data_processing import process_data, prepare_dataframe, add_total_row
from image.image_operations import handle_image_operations, upload_qr_code_barcode, add_qr_code_and_barcode
from download.download_operations import handle_download
from processing.consumo import calculate_consumption_generation
from processing.savings_carbon import calculate_total_savings_and_carbon_emissions
from data.load_data import load_data
from helpers.utils import ordenar_periodo
from helpers.helpers import (
    calcular_valores, calcular_vencimento, calcular_mes_referencia
)
from helpers.ui_helpers import (
    selecionar_periodo_e_loja, confirmar_periodo_lojas_button, calcular_por_recebimento_button,
    calcular_por_compensacao_button, ajustar_valores_kwh_e_desconto, confirmar_valores_button,
    selecionar_cliente, confirmar_cliente_button, confirmar_data_upload_button
)

# Carregar o conteúdo do arquivo CSS
def load_css(file_name):
    # Abre o arquivo CSS e aplica o estilo à aplicação Streamlit
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Chamar a função para carregar o CSS
load_css('styles/styles.css')

# Configura o título da aplicação Streamlit.
st.title("Processamento de Dados de Energia")

# Carrega os dados através de uma função personalizada.
df = load_data()

# Verifica se o DataFrame não está vazio e contém as colunas necessárias
if not df.empty and 'Período' in df.columns and 'Modalidade' in df.columns:
    # Seleciona o período e a loja desejada
    data_desejada, numero_instalacao = selecionar_periodo_e_loja(df)
    
    if numero_instalacao and data_desejada is not None:
        # Filtra os dados com base na data e na loja selecionadas
        df_filtered2 = df[(df['Período'] == data_desejada) & (df['Modalidade'].isin(numero_instalacao))]
        df_filtered2 = df_filtered2[df_filtered2['Modalidade'] != 'Auto Consumo-Geradora']

        # Exibe os dados filtrados
        st.write("Dados Filtrados:", df_filtered2)

        # Calcula o total de recebimentos e compensações
        RECEBIDO_RECEBIMENTO = int(df_filtered2['Recebimento'].sum())
        RECEBIDO_COMPENSACAO = int(df_filtered2['Compensação'].sum())

        # Botão para confirmar o período e as lojas selecionadas
        confirmar_periodo_lojas_button(data_desejada, numero_instalacao)

        # Cria duas colunas para os botões de cálculo
        col1, col2 = st.columns(2)

        with col1:
            # Botão para calcular por recebimento
            calcular_por_recebimento_button(RECEBIDO_RECEBIMENTO)

        with col2:
            # Botão para calcular por compensação
            calcular_por_compensacao_button(RECEBIDO_COMPENSACAO)

        # Exibe informações sobre o período e a loja selecionados
        if 'numero_instalacao' in st.session_state and 'data_desejada' in st.session_state:
            st.write(f"Período Referência selecionado: {st.session_state.data_desejada}")
            st.write(f"Lojas desejadas: {st.session_state.numero_instalacao}")
            if 'calculo_tipo' in st.session_state and 'RECEBIDO' in st.session_state:
                st.write(f"Cálculo selecionado: {st.session_state.calculo_tipo}")
                st.write(f"Qtde kWh faturado: {st.session_state.RECEBIDO} kWh")
            else:
                st.warning("Selecione o tipo de cálculo primeiro.")

        # Ajusta os valores de kWh e desconto
        if 'data_desejada' in st.session_state and 'numero_instalacao' in st.session_state:
            VALOR_KWH_CEMIG_PADRAO = 0.956
            DESCONTO_PADRAO = 20

            # Ajusta os valores de kWh da Cemig e o percentual de desconto
            VALOR_KWH_CEMIG, DESCONTO = ajustar_valores_kwh_e_desconto(VALOR_KWH_CEMIG_PADRAO, DESCONTO_PADRAO)

            # Botão para confirmar os valores ajustados
            confirmar_valores_button(VALOR_KWH_CEMIG, DESCONTO)

            # Calcula o valor de kWh faturado
            VALOR_KWH_FATURADO = calcular_valores(VALOR_KWH_CEMIG, DESCONTO)

            # Exibe os valores confirmados
            st.write(f"Valor KWh Cemig confirmado: R${VALOR_KWH_CEMIG}")
            st.write(f"Desconto confirmado: {DESCONTO}%")
            st.write(f"Valor KWh faturado confirmado: R${VALOR_KWH_FATURADO}")

            if 'RECEBIDO' in st.session_state:
                RECEBIDO = st.session_state.RECEBIDO
                VALOR_A_PAGAR = round(RECEBIDO * VALOR_KWH_FATURADO, 2)
                st.write(f"Qtde kWh faturado: {RECEBIDO} kWh ")
                st.write(f"Valor a Pagar: R$ {VALOR_A_PAGAR}")

                # Processa os dados do último mês e calcula a geração mensal
                df_last_month, ultimo_periodo = process_data(df, st.session_state.data_desejada, st.session_state.numero_instalacao)

                calc_type = "Geração" if st.session_state.calculo_tipo == 'Recebimento' else "Compensação"
                df_copy = df.copy()
                monthly_data = calculate_consumption_generation(df_copy, calc_type)
                monthly_data = ordenar_periodo(monthly_data)

                # Exibe o consumo e a geração mensal
                st.write("Consumo e geração mensal:")
                st.dataframe(monthly_data)

                df_copy02 = df.copy()
                df_copy02['Período'] = pd.to_datetime(df_copy02['Período'], format='%m/%Y')

                # Calcula a economia total e a emissão de carbono evitada
                economia_total, carbono_economia = calculate_total_savings_and_carbon_emissions(df_copy02, data_desejada, VALOR_KWH_CEMIG, VALOR_KWH_FATURADO)
               
                st.write(f'Total Economizado do começo dos dados ao mês selecionado: R$ {economia_total:.2f}')
                st.write(f'Total de Carbono não emitido do começo dos dados ao mês selecionado: {carbono_economia:.2f} kg')

                # Seleciona o cliente
                cliente_text = selecionar_cliente()

                # Botão para confirmar o cliente selecionado
                confirmar_cliente_button(cliente_text)

                # Confirma a data de upload
                data_desejada02 = confirmar_data_upload_button()

                # Calcula o vencimento e o mês de referência
                vencimento02 = calcular_vencimento(data_desejada02)
                mes_referencia = calcular_mes_referencia(data_desejada02)

                if len(ultimo_periodo) > 5:
                    ultimo_periodo = ultimo_periodo[:5]
                    ultimo_periodo = datetime.strptime(ultimo_periodo, '%m/%y')

                # Prepara o DataFrame para exibição
                preprocessed_df = prepare_dataframe(df_filtered2, VALOR_KWH_FATURADO, st.session_state.calculo_tipo)
                selected_columns = st.multiselect("Selecione as colunas a serem exibidas:", preprocessed_df.columns, default=preprocessed_df.columns.tolist())
                preprocessed_df_filtered = preprocessed_df[selected_columns] if selected_columns else pd.DataFrame(columns=preprocessed_df.columns)
                preprocessed_df_filtered = add_total_row(preprocessed_df_filtered)

                # Gera a imagem com os dados processados
                img = handle_image_operations(preprocessed_df_filtered, monthly_data, selected_columns, preprocessed_df.columns.tolist(), st.session_state.calculo_tipo, RECEBIDO, VALOR_A_PAGAR, VALOR_KWH_CEMIG, DESCONTO, VALOR_KWH_FATURADO, economia_total, carbono_economia, cliente_text, mes_referencia, vencimento02)

                # Upload de QR Code e código de barras
                qr_code_image_file, barcode_image_file = upload_qr_code_barcode()
                img = add_qr_code_and_barcode(img, qr_code_image_file, barcode_image_file)

                # Manipulação do download dos arquivos gerados
                handle_download(img, cliente_text, VALOR_A_PAGAR)
