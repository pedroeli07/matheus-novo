# Matheus PDF

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-0.84.0+-red.svg)
![GitHub](https://img.shields.io/badge/GitHub-Repository-lightgrey.svg)

## Descrição

**Matheus Novo** é um projeto de processamento de dados de energia, desenvolvido com o objetivo de analisar, calcular e gerar relatórios detalhados sobre consumo, geração, economia e emissões de carbono evitadas. Utiliza-se principalmente **Python** e **Streamlit** para criar uma interface interativa que facilita a visualização e o download de informações.

## Funcionalidades

- **Processamento de Dados de Energia**
- **Filtragem por Período e Loja**
- **Cálculo de Economia e Emissões de Carbono**
- **Geração de Imagens e PDFs**
- **Upload de Imagens de QR Code e Código de Barras**
- **Interface Interativa com Streamlit**

## Estrutura do Projeto

matheus-novo/
│
├── data/
│ ├── data_processing.py
│ ├── load_data.py
│ └── init.py
│
├── download/
│ ├── download_operations.py
│ └── init.py
│
├── helpers/
│ ├── helpers.py
│ ├── ui_helpers.py
│ ├── utils.py
│ └── init.py
│
├── image/
│ ├── image_operations.py
│ └── init.py
│
├── processing/
│ ├── consumo.py
│ ├── savings_carbon.py
│ └── init.py
│
├── styles/
│ └── styles.css
│
├── main.py
└── README.md


## Instalação

### Pré-requisitos

- **Python 3.9+**
- **pip** (gerenciador de pacotes do Python)
- **Git** (para clonar o repositório)

### Passos

1. **Clone o repositório**

    ```bash
    git clone https://github.com/pedroeli07/matheus-novo.git
    cd matheus-novo
    ```

2. **Crie e ative um ambiente virtual**

    ```bash
    python -m venv myvenv
    source myvenv/bin/activate  # No Windows: myvenv\Scripts\activate
    ```

3. **Instale as dependências**

    ```bash
    pip install -r requirements.txt
    ```

4. **Execute a aplicação**

    ```bash
    streamlit run main.py
    ```

## Uso

### Interface do Streamlit

Ao executar o comando `streamlit run main.py`, a interface do Streamlit será aberta no navegador padrão. Aqui estão algumas funcionalidades que você pode usar:

1. **Selecionar Período e Loja**
2. **Confirmar Seleções**
3. **Calcular por Recebimento ou Compensação**
4. **Ajustar Valores de KWh e Desconto**
5. **Visualizar Consumo e Geração Mensal**
6. **Gerar e Baixar Relatórios (Imagem e PDF)**

### Exemplo de Uso

#### Selecionar Período e Loja

Selecione a data desejada e a loja para filtrar os dados:

```python
data_desejada, numero_instalacao = selecionar_periodo_e_loja(df)
