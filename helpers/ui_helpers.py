import streamlit as st
from datetime import datetime

def selecionar_periodo_e_loja(df):
    available_dates = df['Período'].unique()
    data_desejada = st.selectbox("Selecione a data desejada:", available_dates, index=0, key="data_desejada_selectbox")
    available_inst = df['Modalidade'].unique()
    numero_instalacao = st.multiselect("Selecione a loja desejada:", available_inst, key="modalidade_selectbox")
    return data_desejada, numero_instalacao

def confirmar_periodo_lojas_button(data_desejada, numero_instalacao):
    with st.form(key='confirm_period_form'):
        submitted = st.form_submit_button(
            label='Confirmar Período e Lojas',
            help='Confirma o período e as lojas selecionadas'
        )
        if submitted:
            st.session_state.data_desejada = data_desejada
            st.session_state.numero_instalacao = numero_instalacao
            st.success('Período e lojas confirmados!')
        st.markdown("""
            <style>
                .stButton button {
                    background-color: darkred;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 8px;
                }
                .stButton button:hover {
                    background-color: darkgreen;
                }
            </style>
        """, unsafe_allow_html=True)

def calcular_por_recebimento_button(RECEBIDO_RECEBIMENTO):
    with st.form(key='calculate_receipt_form'):
        submitted = st.form_submit_button(
            label='Calcular por Recebimento',
            help='Calcula baseado no recebimento'
        )
        if submitted:
            st.session_state.RECEBIDO = RECEBIDO_RECEBIMENTO
            st.session_state.calculo_tipo = 'Recebimento'
            st.success('Cálculo selecionado: Recebimento')
        st.markdown("""
            <style>
                .stButton button {
                    background-color: blue;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 20px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 8px;
                }
                .stButton button:hover {
                    background-color: darkblue;
                }
            </style>
        """, unsafe_allow_html=True)

def calcular_por_compensacao_button(RECEBIDO_COMPENSACAO):
    with st.form(key='calculate_compensation_form'):
        submitted = st.form_submit_button(
            label='Calcular por Compensação',
            help='Calcula baseado na compensação'
        )
        if submitted:
            st.session_state.RECEBIDO = RECEBIDO_COMPENSACAO
            st.session_state.calculo_tipo = 'Compensação'
            st.success('Cálculo selecionado: Compensação')
        st.markdown("""
            <style>
                .stButton button {
                    background-color: darkblue;
                    color: white;
                    border: none;
                    padding: 15px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 8px;
                }
                .stButton button:hover {
                    background-color: darkred;
                }
            </style>
        """, unsafe_allow_html=True)

def ajustar_valores_kwh_e_desconto(VALOR_KWH_CEMIG_PADRAO, DESCONTO_PADRAO):
    VALOR_KWH_CEMIG = st.number_input("Digite o valor do KWh da Cemig (R$):", min_value=0.1000, max_value=2.00, value=VALOR_KWH_CEMIG_PADRAO, step=0.001, format="%.3f")
    DESCONTO = st.number_input("Digite o valor do desconto (%):", min_value=0, max_value=100, value=DESCONTO_PADRAO, step=1)
    return VALOR_KWH_CEMIG, DESCONTO

def confirmar_valores_button(VALOR_KWH_CEMIG, DESCONTO):
    with st.form(key='confirm_values_form'):
        submitted = st.form_submit_button(
            label='Confirmar Valores'
        )
        if submitted:
            st.session_state.VALOR_KWH_CEMIG = VALOR_KWH_CEMIG
            st.session_state.DESCONTO = DESCONTO
            st.success('Valores confirmados!')
        st.markdown("""
            <style>
                .stButton button {
                    background-color: darkred;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 8px;
                }
                .stButton button:hover {
                    background-color: darkgreen;
                }
            </style>
        """, unsafe_allow_html=True)

def selecionar_cliente():
    nomes_clientes = ['Gracie Barra BH', 'Cliente 2', 'Cliente 3']
    cliente_selecionado = st.selectbox("Selecione ou digite o nome do cliente:", nomes_clientes + ['Outro'])
    if cliente_selecionado == 'Outro':
        cliente_text = st.text_input("Digite o nome do cliente:", value="", placeholder="Digite o nome do cliente aqui")
    else:
        cliente_text = cliente_selecionado
    return cliente_text

def confirmar_cliente_button(cliente_text):
    with st.form(key='confirm_client_form'):
        submitted = st.form_submit_button(
            label='Confirmar Cliente'
        )
        if submitted:
            st.session_state.cliente_text = cliente_text
            st.success('Cliente confirmado!')
        st.markdown("""
            <style>
                .stButton button {
                    background-color: darkred;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 8px;
                }
                .stButton button:hover {
                    background-color: darkgreen;
                }
            </style>
        """, unsafe_allow_html=True)

def confirmar_data_upload_button():
    data_atual = datetime.now()
    data_desejada02 = st.date_input("Selecione a data desejada:", value=data_atual)
    with st.form(key='confirm_upload_date_form'):
        submitted = st.form_submit_button(
            label='Confirmar Data de Upload'
        )
        if submitted:
            st.session_state.data_desejada02 = data_desejada02
            st.success('Data de upload confirmada!')
        st.markdown("""
            <style>
                .stButton button {
                    background-color: green;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 8px;
                }
                .stButton button:hover {
                    background-color: darkgreen;
                }
            </style>
        """, unsafe_allow_html=True)
    return data_desejada02

def upload_qr_code_barcode():
    qr_code_image_file = st.file_uploader("Upload Imagem QR Code", type=["png", "jpeg"])
    barcode_image_file = st.file_uploader("Upload Imagem Código de Barras", type=["png", "jpeg"])
    return qr_code_image_file, barcode_image_file
