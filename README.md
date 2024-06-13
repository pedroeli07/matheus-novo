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
Confirmar Período e Lojas
Confirme as seleções para prosseguir:

python
Copy code
confirmar_periodo_lojas_button(data_desejada, numero_instalacao)
Calcular por Recebimento ou Compensação
Escolha o método de cálculo:

python
Copy code
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

