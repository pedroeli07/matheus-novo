from PIL import ImageFont

# Função para criar uma fonte TrueType
def create_font(fonte_path, size):
    return ImageFont.truetype(fonte_path, size=size)

# Função para retornar todas as fontes disponíveis
def fonts():
    # Dicionário com as fontes e seus respectivos tamanhos
    return {
        "bold1": create_font("fonts/OpenSans-Bold.ttf", 38), # Fonte em negrito com tamanho 38
        "bold2": create_font("fonts/OpenSans-Bold.ttf", 34), # Fonte em negrito com tamanho 34
        "bold3": create_font("fonts/OpenSans-Bold.ttf", 36), # Fonte em negrito com tamanho 36
        "regular1": create_font("fonts/OpenSans-Regular.ttf", 25), # Fonte regular com tamanho 25
        "bold_carb": create_font("fonts/OpenSans-Bold.ttf", 38), # Fonte em negrito com tamanho 38
        "bold_eco": create_font("fonts/OpenSans-Bold.ttf", 40), # Fonte em negrito com tamanho 40
        "bold4": create_font("fonts/OpenSans-Bold.ttf", 49), # Fonte em negrito com tamanho 49
        "bold_df": create_font("fonts/OpenSans-Bold.ttf", 13), # Fonte em negrito com tamanho 13
        "bold_df2": create_font("fonts/OpenSans-Bold.ttf", 15), # Fonte em negrito com tamanho 15
        "extra_bold": create_font("fonts/OpenSans-ExtraBold.ttf", 13), # Fonte em negrito extra com tamanho 13
        "extra_bold2": create_font("fonts/OpenSans-Bold.ttf", 18), # Fonte em negrito com tamanho 18
        "df": create_font("fonts/OpenSans-Regular.ttf", 13), # Fonte regular com tamanho 13
        "bold_df3": create_font("fonts/OpenSans-Bold.ttf", 18), # Fonte em negrito com tamanho 18
        "df3": create_font("fonts/OpenSans-Regular.ttf", 18) # Fonte regular com tamanho 18
    }

