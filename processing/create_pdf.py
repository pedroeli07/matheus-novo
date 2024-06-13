from io import BytesIO
from fpdf import FPDF
import tempfile

def generate_pdf(image):
    """
    Gera um arquivo PDF a partir de uma imagem.

    Args:
        image (PIL.Image.Image): Imagem a ser adicionada ao PDF.

    Returns:
        BytesIO: Objeto BytesIO contendo o PDF gerado.
    """

    # Cria uma instância do objeto FPDF com unidades definidas como pontos e formato definido como 8.28 x 11.69 polegadas
    pdf = FPDF(unit='pt', format=[598.56, 845.28])

    # Adiciona uma nova página ao PDF
    pdf.add_page()

    # Cria um arquivo temporário para salvar a imagem
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        # Salva a imagem no arquivo temporário em formato PNG
        image.save(tmpfile, format='PNG')
        tmpfile_path = tmpfile.name

    # Adiciona a imagem ao PDF, ajustando seu tamanho à página
    pdf.image(tmpfile_path, x=0, y=0, w=598.56, h=845.28)

    # Prepara o PDF para ser retornado como um objeto BytesIO
    pdf_output = BytesIO()

    # Gera o PDF e o codifica em latin1 para ser armazenado no BytesIO
    pdf_output.write(pdf.output(dest='S').encode('latin1'))

    # Reposiciona o cursor no início do BytesIO para permitir a leitura
    pdf_output.seek(0)

    return pdf_output



