def format_value(value):
    """
    Converte um valor em string para um valor numérico e arredonda para duas casas decimais, caso necessário.

    :param value: O valor em string a ser convertido.
    :return: O valor numérico convertido com arredondamento para duas casas decimais, caso necessário.
    """
    try:
        # Tenta converter o valor em string para um valor numérico
        value = float(value)

        # Verifica se o valor é um número inteiro
        if value.is_integer():
            # Caso seja, retorna o valor como um número inteiro
            return int(value)
        else:
            # Caso contrário, arredonda o valor para duas casas decimais e retorna
            return round(value, 2)
    except (ValueError, TypeError):
        # Caso não seja possível converter o valor em um número, retorna o valor original
        return value

def format_currency(value):
    """
    Formata um valor numérico como moeda no formato 'R$ X,XX', onde X é um número inteiro e XX é um número de duas casas decimais.

    :param value: O valor numérico a ser formatado.
    :return: O valor formatado como moeda no formato 'R$ X,XX'.
    """
    # Formata o valor como moeda no formato 'R$ X,XX'
    formatted_value = f"R$ {value:,.2f}"

    # Substitui a vírgula por 'X' para permitir a formatação correta
    formatted_value = formatted_value.replace(',', 'X')

    # Substitui o ponto por vírgula para obter o formato desejado 'R$ X,XX'
    formatted_value = formatted_value.replace('.', ',')

    # Substitui 'X' por vírgula para obter o formato final correto 'R$ X,XX'
    formatted_value = formatted_value.replace('X', '.')

    # Retorna o valor formatado como moeda no formato 'R$ X,XX'
    return formatted_value
