from PIL import Image
from io import BytesIO
import streamlit as st
from processing.create_pdf import generate_pdf

def handle_download(img, cliente_text, VALOR_A_PAGAR):
    # Salva a imagem no buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")

    # Cria um botão para baixar a imagem
    st.download_button(
        label="Baixar Imagem",  # Texto do botão
        data=buffer,  # Conteúdo do arquivo a ser baixado
        file_name="imagem_processada.png",  # Nome do arquivo a ser baixado
        mime="image/png",  # Tipo de arquivo a ser baixado
        key="download_image_button"
    )

    # Cria botões para gerar a imagem e o PDF
    generate_image_button = st.button("Gerar Imagem", key="generate_image_button")
    generate_pdf_button = st.button("Gerar PDF", key="generate_pdf_button")

    # Verifica se o botão para gerar a imagem foi clicado
    if generate_image_button:
        st.image(img, caption='Imagem Gerada', use_column_width=True)  # Exibe a imagem

    # Verifica se o botão para gerar o PDF foi clicado
    if generate_pdf_button:
        # Gera o PDF com a imagem
        pdf_output = generate_pdf(img)

        # Cria um botão para baixar o PDF
        st.download_button(
            label="Baixar PDF",  # Texto do botão
            data=pdf_output,  # Conteúdo do arquivo a ser baixado
            file_name=f"{cliente_text}{VALOR_A_PAGAR}.pdf",  # Nome do arquivo a ser baixado
            mime="application/pdf",  # Tipo de arquivo a ser baixado
            key="download_pdf_button"
        )
