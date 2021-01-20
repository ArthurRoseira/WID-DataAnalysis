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


##########################################
#
# Method used to test correlation between two
# time series
#
##########################################

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
    return dataPlot


def correlation(dataPlot):
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


def autocorrelation(data):
    #######################
    # Testing two methods of
    # Autocorrelation Visualization
    #######################
    print(data.head(10))
    plt.figure(figsize=(18, 10))
    ax1 = plt.subplot2grid((3, 1), (0, 0))
    ax2 = plt.subplot2grid((3, 1), (1, 0))
    ax3 = plt.subplot2grid((3, 1), (2, 0))

    sns.barplot(y=data.iloc[:, 0].values,
                x=data.index, ax=ax1)
    ax1.set_title('USA Federal Military Exp Series')
    #### First Method #####
    # Lag 0 means autocorrelation of an observation itself
    lag = list(range(0, len(data.iloc[:, 0])))
    autCor = [data.iloc[:, 0].autocorr(l) for l in lag]
    sns.pointplot(x=lag, y=autCor, markers='.', ax=ax2)
    ax2.set_title('Autocorrelation Fed Exp')
    ax2.set_xlabel('Lag(year)')
    ax2.set_ylabel('Autocorrelation')
    ax2.set_xticklabels(lag, rotation=90)

    #### Second Method #####
    r = data.iloc[27, 0]
    plot_acf(data.iloc[:, 0], lags=len(data.iloc[:, 0])-1, zero=False, ax=ax3)
    ax3.set_title('Autocorrelation Fed Exp (plot_acf)')
    ax3.set_xlabel('Lag(year)')
    ax3.set_ylabel('Autocorrelation')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    dataPlot = timedSeries()
    autocorrelation(dataPlot)
