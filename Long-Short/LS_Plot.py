# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:28:04 2021

@author: luciano
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from arch.unitroot import ADF
import LS_cointegracao

import yfinance as yf 

ativo_x = input('Ativo Independente: ')
ativo_y = input('Ativo Dependente: ')
cond=True
periodos = []
while (cond==True):
    periodos.append(int(input('Entre com o período: ')))
    sim_nao = str(input('Deseja inserir mais um período? (s/n): '))
    if sim_nao == 'n':
        cond=False
                 

lista_ativos = [ativo_x, ativo_y]
df = yf.download(tickers = lista_ativos, period='2y', interval='1d', auto_adjust=True)
df = df['Close']
df.reset_index(inplace=True)
df.dropna(axis=0, how='any', inplace=True)
# Resultados
for periodo in periodos:
    resultado = LS_cointegracao.coint_period(df, ativo_x, ativo_y, period = periodo)
    print('Ativo Y: {} Ativo X: {} - Periodo: {}'.format(ativo_y[:-3], ativo_x[:-3], periodo))
    for key in resultado:
        print(key, ': ', resultado[key])
    print('-------------------------------------')
    
# Plots
for periodo in periodos:
    LS_cointegracao.plot(df, ativo_x, ativo_y, period = periodo, tipo = 'residuos', save=False)
    LS_cointegracao.plot(df, ativo_x, ativo_y, period = periodo, tipo = 'fechamento', save=False)
    LS_cointegracao.plot(df, ativo_x, ativo_y, period = periodo, tipo = 'spread', save=False)
    LS_cointegracao.plot(df, ativo_x, ativo_y, period = periodo, tipo = 'regression', save=False)
