import streamlit as st
from datetime import datetime

def load_css():
    with open('styles/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def selecionar_periodo_e_loja(df):
    available_dates = df['Período'].unique()
    st.markdown("<h8 style='color: #8cf595;'>-----------------------------------------Selecione o período que deseja filtrar-------------------------------------------------- </h8>", unsafe_allow_html=True)

    data_desejada = st.selectbox("", available_dates, index=0, key="data_desejada_selectbox")
    st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 </h5>", unsafe_allow_html=True)

    available_inst = df['Modalidade'].unique()
    st.markdown("<h8 style='color: #8cf595;'>-----------------------------------------Selecione as lojas que deseja filtrar:-------------------------------------------------- </h8>", unsafe_allow_html=True)

    numero_instalacao = st.multiselect("Selecione a loja desejada:", available_inst, key="modalidade_selectbox")
    return data_desejada, numero_instalacao

def confirmar_periodo_lojas_button(data_desejada, numero_instalacao):
    st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 </h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 </h5>", unsafe_allow_html=True)

    if st.button('Confirmar Período e Lojas', key='confirm_period_lojas'):
        st.session_state.data_desejada = data_desejada
        st.session_state.numero_instalacao = numero_instalacao
        st.success('Período e lojas confirmados!')

def calcular_por_recebimento_button(RECEBIDO_RECEBIMENTO):
    if st.button('Calcular por Recebimento', key='calculate_receipt'):
        st.session_state.RECEBIDO = RECEBIDO_RECEBIMENTO
        st.session_state.calculo_tipo = 'Recebimento'
        st.success('Cálculo selecionado: Recebimento')

def calcular_por_compensacao_button(RECEBIDO_COMPENSACAO):
    if st.button('Calcular por Compensação', key='calculate_compensation'):
        st.session_state.RECEBIDO = RECEBIDO_COMPENSACAO
        st.session_state.calculo_tipo = 'Compensação'
        st.success('Cálculo selecionado: Compensação')

def ajustar_valores_kwh_e_desconto(VALOR_KWH_CEMIG_PADRAO, DESCONTO_PADRAO):
    VALOR_KWH_CEMIG = st.number_input("Digite o valor do KWh da Cemig (R$):", min_value=0.1000, max_value=2.00, value=VALOR_KWH_CEMIG_PADRAO, step=0.001, format="%.3f")
    DESCONTO = st.number_input("Digite o valor do desconto (%):", min_value=0, max_value=100, value=DESCONTO_PADRAO, step=1)
    return VALOR_KWH_CEMIG, DESCONTO

def confirmar_valores_button(VALOR_KWH_CEMIG, DESCONTO):
    with st.form(key='confirm_values_form'):
        submitted = st.form_submit_button(label='Confirmar Valores')
        if submitted:
            st.session_state.VALOR_KWH_CEMIG = VALOR_KWH_CEMIG
            st.session_state.DESCONTO = DESCONTO
            st.success('Valores confirmados!')

def selecionar_cliente():
    nomes_clientes = ['Gracie Barra BH', 'Cliente 2', 'Cliente 3']
    cliente_selecionado = st.selectbox("Selecione ou digite o nome do cliente:", nomes_clientes + ['Outro'], key='select_cliente')
    return cliente_selecionado if cliente_selecionado != 'Outro' else st.text_input("Digite o nome do cliente:", key='input_cliente')

def confirmar_cliente_button(cliente_text):
    if st.button('Confirmar Cliente', key='confirm_cliente'):
        st.session_state.cliente_text = cliente_text
        st.success('Cliente confirmado!')

def confirmar_data_upload_button():
    data_atual = datetime.now()
    data_desejada02 = st.date_input("Selecione a data desejada:", value=data_atual, key='data_upload')
    if st.button('Confirmar Data de Upload', key='confirm_upload_date'):
        st.session_state.data_desejada02 = data_desejada02
        st.success('Data de upload confirmada!')
    return data_desejada02

def upload_qr_code_barcode():
    qr_code_image_file = st.file_uploader("Upload Imagem QR Code", type=["png", "jpeg"], key='upload_qr')
    barcode_image_file = st.file_uploader("Upload Imagem Código de Barras", type=["png", "jpeg"], key='upload_barcode')
    return qr_code_image_file, barcode_image_file

def render_buttons(data_desejada, numero_instalacao, RECEBIDO_RECEBIMENTO, RECEBIDO_COMPENSACAO):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        confirmar_periodo_lojas_button(data_desejada, numero_instalacao)
        cols = st.columns(2)
        with cols[0]:
            calcular_por_recebimento_button(RECEBIDO_RECEBIMENTO)
        with cols[1]:
            calcular_por_compensacao_button(RECEBIDO_COMPENSACAO)
