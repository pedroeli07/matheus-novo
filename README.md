# Matheus PDF

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-0.84.0+-red.svg)
![GitHub](https://img.shields.io/badge/GitHub-Repository-lightgrey.svg)

## Descrição

**Matheus PDF** é um projeto voltado para o processamento e manipulação de dados de energia, desenvolvido com o objetivo de analisar, calcular e gerar relatórios detalhados sobre consumo, geração, economia e emissões de carbono evitadas. Utiliza-se principalmente **Python** e **Streamlit** para criar uma interface interativa que facilita a visualização, manipulação de imagens e geração de boletos de contas de energia em formato PDF.

## Funcionalidades

- **Processamento de Dados de Energia**
- **Filtragem por Período e Loja**
- **Cálculo de Economia e Emissões de Carbono**
- **Geração de Imagens e PDFs**
- **Upload de Imagens de QR Code e Código de Barras**
- **Interface Interativa com Streamlit**

## Estrutura do Projeto

```plaintext
matheus-novo/
│
├── data/
│   ├── data_processing.py
│   ├── load_data.py
│   └── __init__.py
│
├── download/
│   ├── download_operations.py
│   └── __init__.py
│
├── helpers/
│   ├── helpers.py
│   ├── ui_helpers.py
│   ├── utils.py
│   └── __init__.py
│
├── image/
│   ├── image_operations.py
│   └── __init__.py
│
├── processing/
│   ├── consumo.py
│   ├── savings_carbon.py
│   └── __init__.py
│
├── styles/
│   └── styles.css
│
├── main.py
└── README.md



## Instalação

### Pré-requisitos

- **Python 3.9+**
- **pip** (gerenciador de pacotes do Python)
- **Git** (para clonar o repositório)

Passos
Clone o repositório

```plaintext
git clone https://github.com/pedroeli07/matheus-novo.git
cd matheus-novo

## Crie e ative um ambiente virtual

```plaintext
python -m venv myvenv
source myvenv/bin/activate  # No Windows: myvenv\Scripts\activate

##
Instale as dependências

bash
Copy code
pip install -r requirements.txt
Execute a aplicação

bash
Copy code
streamlit run main.py
Uso
Interface do Streamlit
Ao executar o comando streamlit run main.py, a interface do Streamlit será aberta no navegador padrão. Aqui estão algumas funcionalidades que você pode usar:

Selecionar Período e Loja
Confirmar Seleções
Calcular por Recebimento ou Compensação
Ajustar Valores de KWh e Desconto
Visualizar Consumo e Geração Mensal
Gerar e Baixar Relatórios (Imagem e PDF)
Exemplo de Uso
Selecionar Período e Loja
Selecione a data desejada e a loja para filtrar os dados:

python
Copy code
data_desejada, numero_instalacao = selecionar_periodo_e_loja(df)
confirmar_periodo_lojas_button(data_desejada, numero_instalacao)
calcular_por_recebimento_button(RECEBIDO_RECEBIMENTO)
calcular_por_compensacao_button(RECEBIDO_COMPENSACAO)
Ajustar Valores
Ajuste os valores de KWh da Cemig e o percentual de desconto:

python
Copy code
VALOR_KWH_CEMIG, DESCONTO = ajustar_valores_kwh_e_desconto(VALOR_KWH_CEMIG_PADRAO, DESCONTO_PADRAO)
confirmar_valores_button(VALOR_KWH_CEMIG, DESCONTO)
Visualizar Consumo e Geração Mensal
Visualize o consumo e a geração mensal de energia:

python
Copy code
monthly_data = calculate_consumption_generation(df_copy, calc_type)
st.dataframe(monthly_data)
Gerar e Baixar Relatórios
Gere e baixe os relatórios em imagem e PDF:

python
Copy code
handle_download(img, cliente_text, VALOR_A_PAGAR)
Contribuição
Sinta-se à vontade para contribuir com o projeto! Veja abaixo como você pode ajudar:

Faça um fork do projeto
Crie uma branch para sua feature (git checkout -b feature/sua-feature)
Faça commit das suas alterações (git commit -m 'Adiciona sua feature')
Faça push para a branch (git push origin feature/sua-feature)
Abra um Pull Request
Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

Contato
Pedro Eli - GitHub
