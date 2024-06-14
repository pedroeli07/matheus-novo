import pandas as pd

# Função para estilizar o DataFrame
def style_dataframe(df):
    styles = [
        {'selector': 'thead th', 
         'props': [('background-color', '#2c3e50'), 
                   ('color', 'white'), 
                   ('font-family', 'Arial'), 
                   ('font-size', '16px')]},
        {'selector': 'tbody tr:nth-child(even)', 
         'props': [('background-color', '#f2f2f2')]},
        {'selector': 'tbody tr:nth-child(odd)', 
         'props': [('background-color', '#ffffff')]},
        {'selector': 'tbody td', 
         'props': [('color', '#2c3e50'), 
                   ('font-family', 'Arial'), 
                   ('font-size', '14px'), 
                   ('border', '1px solid #ddd')]},
        {'selector': 'tbody td:hover', 
         'props': [('background-color', '#d5d8dc')]}
    ]
    
    styled_df = df.style.set_table_styles(styles)
    return styled_df
