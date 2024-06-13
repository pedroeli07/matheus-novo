from PIL import Image, ImageDraw
import pandas as pd
from helpers.utils import ordenar_periodo
from fonts.fontys import fonts
from data.formaters import format_value, format_currency


def add_text(draw, text, position, font, fill="black"):
    draw.text(position, text, fill=fill, font=font)

def draw_rectangle(draw, coords, fill, outline="black"):
    draw.rectangle(coords, fill=fill, outline=outline)

def generate_image(preprocessed_df, monthly_data, selected_columns, default_columns, calculo_tipo, RECEBIDO, VALOR_A_PAGAR, VALOR_KWH_CEMIG, DESCONTO, VALOR_KWH_FATURADO, economia_total, carbono_economia, cliente_text, mes_referencia, vencimento02):
    img = Image.open('boleto_padrao04.png')
    draw = ImageDraw.Draw(img)
    fontys = fonts()  # Carregar as fontes

    # Formatação de valores
    recebido_text = f"{int(RECEBIDO):,d}".replace(',', '.')
    pos_x = 912 - (len(recebido_text) - 4) * 20
    texto_acima = "RECEBIDO" if calculo_tipo == 'Recebimento' else "COMPENSADO"
    text_width_acima = draw.textlength(texto_acima, font=fontys["bold3"])
    pos_x_acima = 928 + (100 - text_width_acima) // 2
    add_text(draw, texto_acima, (pos_x_acima, 1108), font=fontys["bold3"])
    add_text(draw, recebido_text, (pos_x, 1168) if len(recebido_text) > 4 else (888, 1168), font=fontys["bold1"])

    add_text(draw, str(mes_referencia), (440, 667), font=fontys["regular1"])
    add_text(draw, str(vencimento02), (360, 702), font=fontys["regular1"])
    add_text(draw, format_currency(economia_total), (1020, 2240), font=fontys["bold_eco"])
    add_text(draw, f"{int(carbono_economia):,d} Kg".replace(',', '.'), (975, 2112), font=fontys["bold_carb"])

    add_text(draw, format_currency(VALOR_A_PAGAR), (880, 1407), font=fontys["bold1"])
    add_text(draw, "VALOR A PAGAR", (850, 1337), font=fontys["bold2"])

    add_text(draw, cliente_text, (297, 631), font=fontys["regular1"])
    add_text(draw, str(VALOR_KWH_CEMIG), (740, 663), font=fontys["bold4"])
    add_text(draw, str(VALOR_KWH_FATURADO), (1310, 663), font=fontys["bold4"])

    desconto_text = str(int(DESCONTO))
    desconto_x = 970 if len(desconto_text) > 2 else 1015 if len(desconto_text) < 2 else 990
    add_text(draw, desconto_text, (desconto_x, 663), font=fontys["bold4"])

    # Processamento de DataFrame
    monthly_data = ordenar_periodo(monthly_data).iloc[-12:]
    dataframe_position1 = (225, 1130)
    cell_width_df1, cell_height_base1, max_height1 = 180, 90, 330
    num_rows = len(monthly_data) or 1
    cell_height_df1 = min(cell_height_base1, max_height1 // num_rows)
    for j, column_name in enumerate(monthly_data.columns):
        draw_rectangle(draw, [(dataframe_position1[0] + j * cell_width_df1, dataframe_position1[1]),
                              (dataframe_position1[0] + (j + 1) * cell_width_df1, dataframe_position1[1] + cell_height_df1)], 
                              "#c1f0f0")
        text_width = draw.textlength(column_name, font=fontys["bold_df2"])
        add_text(draw, column_name, (dataframe_position1[0] + j * cell_width_df1 + (cell_width_df1 - text_width) // 2 , dataframe_position1[1] + 5), font=fontys["bold_df2"])
    
    for i, (_, row) in enumerate(monthly_data.iterrows()):
        for j, cell_value in enumerate(row):
            background_color = "#c1e0ff" if i == len(monthly_data) - 1 else "#F0F0F0"
            draw_rectangle(draw, [(dataframe_position1[0] + j * cell_width_df1, dataframe_position1[1] + (i + 1) * cell_height_df1),
                                  (dataframe_position1[0] + (j + 1) * cell_width_df1, dataframe_position1[1] + (i + 2) * cell_height_df1)], 
                                  background_color)
            cell_text = str(format_value(cell_value)).upper() if i == len(monthly_data) - 1 and monthly_data.columns[j] == "Período" else str(format_value(cell_value))
            text_font = fontys["extra_bold2"] if i == len(monthly_data) - 1 else fontys["df"]
            text_width = draw.textlength(cell_text, font=text_font)
            add_text(draw, cell_text, (dataframe_position1[0] + j * cell_width_df1 + (cell_width_df1 - text_width) // 2, dataframe_position1[1] + (i + 1) * cell_height_df1 + (cell_height_df1 - text_font.size) // 2), text_font)

    # Ajuste de DataFrame com as colunas selecionadas
    dataframe_position, total_width, max_height, cell_height_base = (220, 870), 1250, 115, 90
    cell_width_df = total_width // len(selected_columns) if selected_columns else total_width
    preprocessed_df = preprocessed_df[selected_columns] if selected_columns else pd.DataFrame(columns=default_columns)
    num_rows = len(preprocessed_df) or 1
    cell_height_df = min(cell_height_base, max_height // num_rows)
    
    for j, column_name in enumerate(preprocessed_df.columns):
        draw_rectangle(draw, [(dataframe_position[0] + j * cell_width_df, dataframe_position[1]),
                              (dataframe_position[0] + (j + 1) * cell_width_df, dataframe_position[1] + cell_height_df)], 
                              "#c1f0f0")
        text_width = draw.textlength(column_name, font=fontys["bold_df3"])
        add_text(draw, column_name, (dataframe_position[0] + j * cell_width_df + (cell_width_df - text_width) // 2, dataframe_position[1] + (cell_height_df - fontys["bold_df3"].size) // 2), font=fontys["bold_df3"])
    
    for i, (_, row) in enumerate(preprocessed_df.iterrows()):
        background_color = "#c1e0ff" if i == len(preprocessed_df) - 1 else "white"
        text_font = fontys["extra_bold2"] if i == len(preprocessed_df) - 1 else fontys["df3"]
        for j, cell_value in enumerate(row):
            cell_text = str(format_value(cell_value))
            text_width = draw.textlength(cell_text, font=text_font)
            draw_rectangle(draw, [(dataframe_position[0] + j * cell_width_df, dataframe_position[1] + (i + 1) * cell_height_df),
                                  (dataframe_position[0] + (j + 1) * cell_width_df, dataframe_position[1] + (i + 2) * cell_height_df)], 
                                  background_color)
            add_text(draw, cell_text, (dataframe_position[0] + j * cell_width_df + (cell_width_df - text_width) // 2, dataframe_position[1] + (i + 1) * cell_height_df + (cell_height_df - text_font.size) // 2), text_font)

    return img
