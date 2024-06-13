from PIL import Image
from helpers.helpers import preparar_imagem, exibir_imagem
from image.image import generate_image
import streamlit as st

def handle_image_operations(preprocessed_df_filtered, monthly_data, selected_columns, default_columns, calculo_tipo, RECEBIDO, VALOR_A_PAGAR, VALOR_KWH_CEMIG, DESCONTO, VALOR_KWH_FATURADO, economia_total, carbono_economia, cliente_text, mes_referencia, vencimento02):
    img = generate_image(preprocessed_df_filtered, monthly_data, selected_columns, default_columns, calculo_tipo, RECEBIDO, VALOR_A_PAGAR, VALOR_KWH_CEMIG, DESCONTO, VALOR_KWH_FATURADO, economia_total, carbono_economia, cliente_text, mes_referencia, vencimento02)
    exibir_imagem(img)
    return img

def upload_qr_code_barcode():
    qr_code_image_file = st.file_uploader("Upload Imagem QR Code", type=["png", "jpeg"])
    barcode_image_file = st.file_uploader("Upload Imagem Código de Barras", type=["png", "jpeg"])
    return qr_code_image_file, barcode_image_file

def add_qr_code_and_barcode(img, qr_code_image_file, barcode_image_file):
    if qr_code_image_file and barcode_image_file:
        qr_code_image = Image.open(qr_code_image_file)
        barcode_image = Image.open(barcode_image_file)
        img = preparar_imagem(img, qr_code_image, barcode_image)
        img.save('boleto_com_qrcode01.png')
    return img
