import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
import pandas as pd

def confirmar_periodo_lojas(data_desejada, numero_instalacao):
    st.session_state.data_desejada = data_desejada
    st.session_state.numero_instalacao = numero_instalacao
    st.success('Período e lojas confirmados!')

def confirmar_valores(VALOR_KWH_CEMIG, DESCONTO):
    st.session_state.VALOR_KWH_CEMIG = VALOR_KWH_CEMIG
    st.session_state.DESCONTO = DESCONTO
    st.success('Valores confirmados!')

def confirmar_cliente(cliente_text):
    st.session_state.cliente_text = cliente_text
    st.success('Cliente confirmado!')

def confirmar_data_upload(data_desejada02):
    st.session_state.data_desejada02 = data_desejada02
    st.success('Data de upload confirmada!')

def calcular_valores(VALOR_KWH_CEMIG, DESCONTO):
    return round(VALOR_KWH_CEMIG - ((VALOR_KWH_CEMIG * DESCONTO) / 100), 3)

def calcular_vencimento(data_desejada02):
    return (data_desejada02 + timedelta(days=7)).strftime("%d/%m/%Y")

def calcular_mes_referencia(data_desejada02):
    return (data_desejada02.replace(day=1) - timedelta(days=1)).strftime("%m/%Y")

def preparar_imagem(img, qr_code_image, barcode_image):
    proporcao_qr_code = 285 / max(qr_code_image.width, qr_code_image.height)
    proporcao_codigo_barras = 1250 / max(barcode_image.width, barcode_image.height)
    qr_code_image = qr_code_image.resize((int(qr_code_image.width * proporcao_qr_code), int(qr_code_image.height * proporcao_qr_code)))
    barcode_image = barcode_image.resize((int(barcode_image.width * proporcao_codigo_barras), int(barcode_image.height * proporcao_codigo_barras)))
    posicao_x_qr_code = 1205
    posicao_y_qr_code = 1200
    posicao_x_codigo_barras = 225
    posicao_y_codigo_barras = 1600
    img.paste(qr_code_image, (posicao_x_qr_code, posicao_y_qr_code))
    img.paste(barcode_image, (posicao_x_codigo_barras, posicao_y_codigo_barras))
    return img

def exibir_imagem(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    st.image(img, caption="Imagem gerada")
    st.download_button(label="Baixar Imagem", data=buffer, file_name="imagem_processada.png", mime="image/png")
