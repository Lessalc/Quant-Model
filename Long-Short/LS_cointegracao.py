# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 00:50:10 2021

@author: luciano
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from arch.unitroot import ADF


def pares(dados, intervalo = [100, 120, 140, 160, 180, 200, 220, 250], char_excluido=-3, min_period = 5):
    
    coluna_df = ['Ativo_Independente', 'Ativo_Dependente', 'ADF-100', 'ADF-120', 'ADF-140', 'ADF-160',
             'ADF-180', 'ADF-200', 'ADF-220', 'ADF-250', 'Total']
    df = pd.DataFrame(columns = coluna_df)
    m = 0
    for i in range(len(dados.columns)):
        ativo_x = dados.columns[i][:char_excluido]
        
        for j in range(len(dados.columns)):
            if j != i:
                ativo_y = dados.columns[j][:char_excluido]
                
                par = dados.iloc[:,[i,j]]
                
                df.loc[m, 'Ativo_Independente'] = ativo_x
                df.loc[m, 'Ativo_Dependente'] = ativo_y
                
                ####################### ESCOLHENDO O INTERVALO ########################
                l_ini = len(par.index)
                
                k = 2
                soma = 0
                for n in intervalo:
                    par_n = par.iloc[l_ini-n:,:]
                
                
                    ##############################################################
                    
                    ###### REGRESSÃO E RESÍDUOS #################################
                    X = par_n.iloc[:, 0].values
                    y = par_n.iloc[:, 1].values
                    X = X.reshape(-1, 1)
                    modelo = LinearRegression()
                    modelo.fit(X,y)                
                    y_pred = modelo.predict(X)                
                    residuos = y - y_pred                
                    adf = ADF(residuos)
                    if adf.stat < adf.critical_values['5%']:
                        df.iloc[m,k] = float(adf.stat)
                        soma = soma + 1
                    else:
                        df.iloc[m,k] = 0
                    
                    k = k+1
                
                df.loc[m,'Total'] = soma
                m = m + 1 
    df = df.loc[df['Total'] >= min_period, :]
    return df


def classificacao_residuos(ativos, dados, intervalo = [100, 120, 140, 160, 180, 200, 220, 250], char_excluido=-3):
    coluna_df = ['Ativo_Independente', 'Ativo_Dependente', 'CoefAng -100p', 'Inters -100p', 'med_res -100p', 'desv_res -100p', 'Adf-Stats-100p', 
             'CoefAng -120p', 'Inters -120p', 'med_res -120p', 'desv_res -120p', 'Adf-Stats-120p',
             'CoefAng -140p', 'Inters -140p', 'med_res -140p', 'desv_res -140p', 'Adf-Stats-140p',
             'CoefAng -160p', 'Inters -160p', 'med_res -160p', 'desv_res -160p', 'Adf-Stats-160p',
             'CoefAng -180p', 'Inters -180p', 'med_res -180p', 'desv_res -180p', 'Adf-Stats-180p',
             'CoefAng -200p', 'Inters -200p', 'med_res -200p', 'desv_res -200p', 'Adf-Stats-200p',
             'CoefAng -220p', 'Inters -220p', 'med_res -220p', 'desv_res -220p', 'Adf-Stats-220p',
             'CoefAng -250p', 'Inters -250p', 'med_res -250p', 'desv_res -250p', 'Adf-Stats-250p']
    df = pd.DataFrame(columns = coluna_df)
    
    ativos_array = np.array([ativos['Ativo_Independente'].values, ativos['Ativo_Dependente'].values])
    
    for i in range(len(ativos)):

        ativo_x = dados.loc[:, str(ativos_array[0,i]+'.SA')]
    
        ativo_y = dados.loc[:, str(ativos_array[1,i]+'.SA')]
    
    
        par = pd.merge(ativo_x, ativo_y, how='inner', on='Date')
    
        df.loc[i, 'Ativo_Independente'] = ativos_array[0,i]
        df.loc[i, 'Ativo_Dependente'] = ativos_array[1,i]
    
        l_ini = len(par.index)
        intervalo = [100,120,140,160,180,200,220,250]
        k = 2
    
    
        for n in intervalo:
            par_n = par.iloc[l_ini-n:,:]
    
            X = par_n.iloc[:, 0].values
            y = par_n.iloc[:, 1].values
    
            X = X.reshape(-1, 1)
            modelo = LinearRegression()
            modelo.fit(X,y)
    
            y_pred = modelo.predict(X)
    
            residuos = y - y_pred
    
            adf = ADF(residuos)
    
            if adf.stat < adf.critical_values['5%']:
                df.iloc[i,k] = float(modelo.coef_)
                k += 1
                df.iloc[i,k] = float(modelo.intercept_)
                k += 1
                df.iloc[i,k] = np.mean(residuos)
                k += 1
                df.iloc[i,k] = np.std(residuos)
                k += 1
                if adf.stat < adf.critical_values['1%']:
                    df.iloc[i,k] = '99'
                else: df.iloc[i,k] = '95'
                k += 1
            else:
                df.iloc[i,k] = 0
                k += 1
                df.iloc[i,k] = 0
                k += 1
                df.iloc[i,k] = 0
                k += 1
                df.iloc[i,k] = 0
                k += 1
                df.iloc[i,k] = '<90'
                k += 1
    return df
      


def coint_period(dados, ativo_x, ativo_y, period = 100, model = False):
    X = dados.loc[:, ativo_x].values[-period:]
    y = dados.loc[:, ativo_y].values[-period:]   
    X = X.reshape(-1, 1)
    modelo = LinearRegression()
    modelo.fit(X,y)
    y_pred = modelo.predict(X)
    residuos = y - y_pred
    adf = ADF(residuos)
    coint99 = adf.stat < adf.critical_values['1%']
    coint95 = adf.stat < adf.critical_values['5%']
    result = {'coef':float(modelo.coef_), 'intercept':float(modelo.intercept_),
              'media_res':np.mean(residuos), 'desvio_res':np.std(residuos),
              'adf_stats':adf.stat, 'Coint_99':coint99, 'Coint_95':coint95}
    
    if model == True:
        return modelo, y_pred, residuos, np.mean(residuos), np.std(residuos)
    else:
        return result
                 
                  
def plot(dados, ativo_x, ativo_y, period = 100, tipo = 'residuos', save=False):
    import matplotlib.pyplot as plt
    modelo, y_pred, residuos, media, desvio = coint_period(dados, ativo_x, ativo_y, period = period, model = True)    
    dados = dados.iloc[-period:, :]
    X = dados.loc[:, ativo_x].values[-period:]
    y = dados.loc[:, ativo_y].values[-period:]
    residuos_padronizado = residuos/np.std(residuos)
    
    if ((tipo == 'residuos') | (tipo == 'Residuos')):
        n = period
        plt.figure(figsize=(15, 6))
        plt.title('Série Temporal Resíduos Padronizada {} períodos'.format(period))
        plt.plot(dados['Date'], residuos_padronizado , color='blue', alpha = 0.6, label='Resíduo Padronizado')
        plt.plot(dados['Date'], np.repeat(media,n) , color='black', linestyle='--')
        plt.plot(dados['Date'], np.repeat(2,n) , color='red', linestyle=':', label='Dois Desvios Padrões')
        plt.plot(dados['Date'], np.repeat(-2,n) , color='red', linestyle=':')
        nome = 'Resíduos_{}_x_{}_{}_periodos.png'.format(ativo_x[:-3], ativo_y[:-3], period)
        plt.legend(loc=0)
        if save==False:
            plt.show()
        else:
            plt.savefig(nome)
    elif ((tipo == 'fechamento') | (tipo == 'Fechamento')):
        plt.title('Preço de Fechamento {} períodos'.format(period))
        plt.plot(dados['Date'], X, color='blue', label=ativo_x)
        plt.plot(dados['Date'], y, color='red', label=ativo_y)
        plt.legend(loc=0)
        nome = 'Fechamento_{}_x_{}_{}_periodos.png'.format(ativo_x[:-3], ativo_y[:-3], period)
        if save==False:
            plt.show()
        else:
            plt.savefig(nome)
    
    elif ((tipo == 'spread') | (tipo == 'Spread')):
        nome = 'Spread_{}_x_{}_{}_periodos.png'.format(ativo_x[:-3], ativo_y[:-3], period)
        plt.title(nome+str(period))
        arr = X/y
        plt.plot(dados['Date'], arr, color='blue', label='Spread')
        if save==False:
            plt.show()
        else:
            plt.savefig(nome)
    elif ((tipo == 'regression') | (tipo == 'Regression')):
        from yellowbrick.regressor import ResidualsPlot
        X = X.reshape(-1, 1)
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 12))
        ax1.set_title('Regressão Linear dos preços')
        ax1.scatter(X, y, color='blue')
        ax1.plot(X, modelo.predict(X), color='red')

        visualizador = ResidualsPlot(modelo, ax= ax2)
        visualizador.fit(X, y)
        visualizador.finalize()
        
        nome = 'Regression_{}_x_{}_{}_periodos.png'.format(ativo_x[:-3], ativo_y[:-3], period)
        if save==False:
            plt.show()
        else:
            plt.savefig(nome)
   
    else:
        lista = ['residuos', 'fechamento', 'spread', 'regression']
        listaM = ['Residuos', 'Fechamento', 'Spread', 'Regression']
        print('Escolha entre as opções abaixo:')
        for i in range(len(lista)):
            print(lista[i], ' ou ', listaM[i])
        
def dados_ativo_profit(ativo, char_excluido=-3):
    colunas = ['Ativo', 'Data', 'Abertura', 'Minimo', 'Maximo', 'Fechamento', 'Vol_Financeira', 'Vol_Neg']
    df_ativo = pd.read_csv(ativo, sep=';', header=None, names=colunas, encoding='latin-1').loc[:,['Data', 'Fechamento']]
    df_ativo['Data'] = pd.to_datetime(df_ativo['Data'], format='%d/%m/%Y')
    df_ativo['Fechamento'] = df_ativo['Fechamento'].str.replace(',','.')
    df_ativo['Fechamento'] = pd.to_numeric(df_ativo['Fechamento'], errors='coerce')
    df_ativo.columns = ['Data', ativo[:char_excluido]]
    df_ativo.sort_values('Data', inplace=True)
    df_ativo.reset_index(inplace=True, drop=True)
    return df_ativo

def precos(dados, char_excluido=-3):
    dados = dados.iloc[-250:]
    colunas = ['Data']+list(dados.columns)
    for i in range(1,len(colunas)):
        colunas[i] = colunas[i][:char_excluido]
    dados.reset_index(inplace=True)
    dados.columns = colunas
    return dados
    


