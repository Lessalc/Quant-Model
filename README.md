## Modelos Quant

- Todos os modelos aqui são baseados em estudos e testes estatísticos
- Não se trata de indicação apenas um hobby

#### Long-Short/

- O objetivo desses códigos é gerar um banco de dados que pode ser usado em planilha do Excel para encontrar oportunidades de Long e Short por cointegração.

- Os códigos obtem dados direto do Yahoo Finance, por meio de uma biblioteca já existente.

- Esse diretório consiste de um projeto completo, com os seguinte códigos:
  - **LongShort.py**
    - Arquivo principal, nele importamos os ativos e os dados e usamos métodos definidos no **LS_cointegracao.py** para realizar o teste de cointegração, filtrar os pares cointegrados e gerar um arquivo CSV
  - **LS_cointegracao.py**
    - Arquivo dedicado a funções que foram usadas nos demais arquivos
  - **LS_Plot.py**
    - Arquivo onde entramos com dois ativos e os períodos que queremos, será gerado o gráfico para cada par
    - Os gráfico que são gerados podem ser observados no Notebook **Long&Short - Cointegração Yahoo.ipynb**

#### Long&Short - Cointegração Yahoo.ipynb

- Notebook resumo explicando como funciona um Long Short por Cointegração

#### Estrategia Setores - IBOV.ipynb

- Notebook testando algumas estratégias com setores do IBOV

