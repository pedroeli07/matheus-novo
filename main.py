import pandas as pd
import streamlit as st
from datetime import datetime
from data.data_processing import process_data, prepare_dataframe, add_total_row
from image.image_operations import handle_image_operations, upload_qr_code_barcode, add_qr_code_and_barcode
from download.download_operations import handle_download
from processing.consumo import calculate_consumption_generation
from processing.savings_carbon import calculate_total_savings_and_carbon_emissions
from data.load_data import load_data
from helpers.utils import ordenar_periodo
from helpers.helpers import calcular_valores, calcular_vencimento, calcular_mes_referencia
from helpers.ui_helpers import *
from styles.style_df import style_dataframe


def load_css():
    with open('styles/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.markdown("<h1 style='color: #8cf595;'>Processando de dados Energéticos</h1>", unsafe_allow_html=True)

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
        
        st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 </h5>", unsafe_allow_html=True)

        # Exibe os dados filtrados
        # Exibe os dados filtrados
        st.markdown("<h2 style='color: #8cf595;'>------------------Dados Filtrados----------------------</h2>", unsafe_allow_html=True)

        def style_dataframe(df):
            styles = [
                {'selector': 'thead th', 
                'props': [('background-color', '#000000'), 
                        ('color', '#ffffff'), 
                        ('font-family', 'Arial'), 
                        ('font-size', '16px')]},
                {'selector': 'tbody tr:nth-child(even)', 
                'props': [('background-color', '#000000')]},
                {'selector': 'tbody tr:nth-child(odd)', 
                'props': [('background-color', '#000000')]},
                {'selector': 'tbody td', 
                'props': [('color', '#000000'), 
                        ('font-family', 'Arial'), 
                        ('font-size', '14px'), 
                        ('border', '1px solid #000000')]},
                {'selector': 'tbody td:hover', 
                'props': [('background-color', '#fa8080')]}
            ]
            
            styled_df = df.style.set_table_styles(styles).set_properties(**{
                'background-color': '#fdd2d2',
                'color': 'white',
                'border-color': 'white'
            })
            return styled_df

        # Aplicar os estilos ao DataFrame
        styled_df = style_dataframe(df_filtered2)

        # Centralizar o DataFrame usando div com estilo CSS
        st.markdown("""
            <div style="display: flex; justify-content: center;">
                {table}
            
        """.format(table=styled_df.to_html()), unsafe_allow_html=True)




        # Calcula o total de recebimentos e compensações
        RECEBIDO_RECEBIMENTO = int(df_filtered2['Recebimento'].sum())
        RECEBIDO_COMPENSACAO = int(df_filtered2['Compensação'].sum())

        # Renderiza os botões centralizados
        render_buttons(data_desejada, numero_instalacao, RECEBIDO_RECEBIMENTO, RECEBIDO_COMPENSACAO)
        
        # Exibe informações sobre o período e a loja selecionados
        if 'numero_instalacao' in st.session_state and 'data_desejada' in st.session_state:
            st.markdown(f"<h5 style='color: #fa8080;'>Período Referência selecionado:</h5> <h5 style='color: #80fa80;'>{st.session_state.data_desejada}</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: #fa8080;'>Lojas desejadas:</h5> <h5 style='color: #80fa80;'>{st.session_state.numero_instalacao}</h5>", unsafe_allow_html=True)
            if 'calculo_tipo' in st.session_state and 'RECEBIDO' in st.session_state:
                st.markdown(f"<h5 style='color: #fa8080;'>Cálculo selecionado:</h5> <h5 style='color: #80fa80;'>{st.session_state.calculo_tipo}</h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='color: #fa8080;'>Qtde kWh faturado:</h5> <h5 style='color: #80fa80;'>{st.session_state.RECEBIDO} kWh</h5>", unsafe_allow_html=True)
            else:
                st.warning("Selecione o tipo de cálculo primeiro.")

        # Ajusta os valores de kWh e desconto
        if 'data_desejada' in st.session_state and 'numero_instalacao' in st.session_state:
            VALOR_KWH_CEMIG_PADRAO = 0.956
            DESCONTO_PADRAO = 20

            # Ajusta os valores de kWh da Cemig e o percentual de desconto
            VALOR_KWH_CEMIG, DESCONTO = ajustar_valores_kwh_e_desconto(VALOR_KWH_CEMIG_PADRAO, DESCONTO_PADRAO)

            # Botão para confirmar os valores ajustados
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                confirmar_valores_button(VALOR_KWH_CEMIG, DESCONTO)

            # Calcula o valor de kWh faturado
            VALOR_KWH_FATURADO = calcular_valores(VALOR_KWH_CEMIG, DESCONTO)

            # Exibe os valores confirmados
            st.markdown(f"<h5 style='color: #fa8080;'>Valor KWh Cemig confirmado:</h5> <h5 style='color: #80fa80;'>R$  {VALOR_KWH_CEMIG}</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: #fa8080;'>Desconto confirmado:</h5> <h5 style='color: #80fa80;'>{DESCONTO} %</h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: #fa8080;'>Valor KWh faturado confirmado:</h5> <h5 style='color: #80fa80;'>R$  {VALOR_KWH_FATURADO}</h5>", unsafe_allow_html=True)

            if 'RECEBIDO' in st.session_state:
                RECEBIDO = st.session_state.RECEBIDO
                VALOR_A_PAGAR = round(RECEBIDO * VALOR_KWH_FATURADO, 2)
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)

                st.markdown(f"<h5 style='color: #fa8080;'>Qtde kWh faturado:</h5> <h5 style='color: #80fa80;'>{RECEBIDO}  kWh</h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)

                st.markdown(f"<h5 style='color: #fa8080;'>Valor a Pagar:</h5> <h5 style='color: #80fa80;'>R$  {VALOR_A_PAGAR}</h5>", unsafe_allow_html=True)
                
                # Processa os dados do último mês e calcula a geração mensal
                df_last_month, ultimo_periodo = process_data(df, st.session_state.data_desejada, st.session_state.numero_instalacao)

                calc_type = "Geração" if st.session_state.calculo_tipo == 'Recebimento' else "Compensação"
                df_copy = df.copy()
                monthly_data = calculate_consumption_generation(df_copy, calc_type)
                monthly_data = ordenar_periodo(monthly_data)
               
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
                # Exibe o consumo e a geração mensal
              #  st.markdown("<h5 style='color: #fa8080;'>Consumo e geração mensal:</h5>", unsafe_allow_html=True)
                st.markdown("<h2 style='color: #8cf595;'>----Consumo e geração mensal----</h2>", unsafe_allow_html=True)

                # Estiliza o DataFrame
                def style_dataframe(df):
                    styles = [
                        {'selector': 'thead th', 
                        'props': [('background-color', '#000000'), 
                                ('color', '#ffffff'), 
                                ('font-family', 'Arial'), 
                                ('font-size', '16px')]},
                        {'selector': 'tbody tr:nth-child(even)', 
                        'props': [('background-color', '#000000')]},
                        {'selector': 'tbody tr:nth-child(odd)', 
                        'props': [('background-color', '#000000')]},
                        {'selector': 'tbody td', 
                        'props': [('color', '#000000'), 
                                ('font-family', 'Arial'), 
                                ('font-size', '14px'), 
                                ('border', '1px solid #000000')]},
                        {'selector': 'tbody td:hover', 
                        'props': [('background-color', '#fa8080')]}
                    ]
                    
                    styled_df = df.style.set_table_styles(styles).set_properties(**{
                        'background-color': '#fdd2d2',
                        'color': 'white',
                        'border-color': 'white'
                    })
                    return styled_df

                # Aplicar os estilos ao DataFrame
                styled_df = style_dataframe(monthly_data)

                # Exibir o DataFrame estilizado no Streamlit
                st.write(styled_df.to_html(), unsafe_allow_html=True)


                df_copy02 = df.copy()
                df_copy02['Período'] = pd.to_datetime(df_copy02['Período'], format='%m/%Y')

                # Calcula a economia total e a emissão de carbono evitada
              
              
                economia_total, carbono_economia = calculate_total_savings_and_carbon_emissions(df_copy02, data_desejada, VALOR_KWH_CEMIG, VALOR_KWH_FATURADO)
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='color: #fa8080;'>Total Economizado do começo dos dados ao mês selecionado:</h5> <h5 style='color: #80fa80;'>R$ {economia_total:.2f}</h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='color: #fa8080;'>Total de Carbono não emitido do começo dos dados ao mês selecionado:</h5> <h5 style='color: #80fa80;'>{carbono_economia:.2f} kg</h5>", unsafe_allow_html=True)

                # Seleciona o cliente
                cliente_text = selecionar_cliente()

                # Botão para confirmar o cliente selecionado
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    confirmar_cliente_button(cliente_text)

                # Confirma a data de upload
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
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
