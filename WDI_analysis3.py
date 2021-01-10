import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from connect import WDI_api
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
import math


def timedSeries():
    wdi = WDI_api()
    data = pd.read_csv('indicators.csv')

    ##### Getting Time Series Data ###########
    centGovDebtCode = data[data.indicatorName ==
                           'Central government debt, total (% of GDP)'].indicatorCode
    mExpCode = data[data.indicatorName ==
                    'Military expenditure (% of GDP)'].indicatorCode
    (info1, govDebtData) = wdi.getData('usa', centGovDebtCode[6920])
    (info2, mExpData) = wdi.getData('usa', mExpCode[9684])
    d1 = govDebtData[['date', 'value']]
    d2 = mExpData[['date', 'value']]
    dataPlot = pd.merge(d1, d2, on='date')
    dataPlot.set_index('date', inplace=True)
    dataPlot.columns = [
        'Federal Military Expenditure', 'Debt of Federal Gov']
    dataPlot.dropna(inplace=True)
    print(dataPlot.head())
    # Array for mena values calculation -> Calc the mean values from de array index 0 to actual point in for loop range (x)
    mean_govDept = [np.mean(np.array(dataPlot['Debt of Federal Gov'])[:x])
                    for x in range(len(np.array(dataPlot['Debt of Federal Gov'])))]
    print(mean_govDept)
    plt.figure(figsize=(18, 4))
    plt.plot(np.array(dataPlot['Debt of Federal Gov']), label='Valor')
    plt.plot(mean_govDept, label='Média')
    plt.title('Série com Média constante')
    plt.legend()
    plt.show()
    # This shows a non stationary series (mean values not constant)
    # Correlation Between two series
    plt.figure(figsize=(18, 4))
    plt.scatter(dataPlot['Debt of Federal Gov'],
                dataPlot['Federal Military Expenditure'])
    plt.xlabel('Gov Dept')
    plt.ylabel('Military Expenditure')
    plt.title('Correlação Divida e Gastos Militares')
    plt.show()


if __name__ == "__main__":
    timedSeries()
