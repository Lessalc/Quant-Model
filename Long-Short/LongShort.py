# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 00:55:34 2021

@author: luciano
"""

import pandas as pd
import LS_cointegracao

import yfinance as yf 

lista_ativos = list(pd.read_csv('https://raw.githubusercontent.com/Lessalc/Long-Short/main/ativos.txt'))
lista_ativos = lista_ativos[:82]
dados = yf.download(tickers = lista_ativos, period='2y', interval='1d', auto_adjust=True)
dados = dados['Close']
dados = dados.loc[dados['^BVSP'].notna(), :]

dados.dropna(axis=1, how='any', inplace=True)
dados.dropna(axis=0, how='any', inplace=True)
dados.drop(columns=['^BVSP'], inplace=True)


#dados = dados.iloc[:, :15]

df = LS_cointegracao.pares(dados)

df_new = LS_cointegracao.classificacao_residuos(df, dados)

df_new.to_csv('pares_cointegrados.csv')

precos = LS_cointegracao.precos(dados)
precos.to_csv('BD_Precos.csv', index=False, header=True)

