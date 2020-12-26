import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from connect import WDI_api


def usaTimeSeriesAnalysis():
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
    print(dataPlot.head())
    dataPlot.set_index('date', inplace=True)
    print(dataPlot.head())
    dataPlot.columns = ['Federal Military Expenditure', 'Debt of Federal Gov']
    print(dataPlot.head())
    dataPlot.dropna(inplace=True)
    print(dataPlot.head())

    #### Plot Time Series #####
    f, ax = plt.subplots(2, sharex=True)
    f.set_size_inches(5.5, 5.5)
    ax[0].set_title('Federal Military Expenditure (% GPD)')
    dataPlot['Federal Military Expenditure'].plot(
        linestyle='-', marker='*', color='b', ax=ax[0])
    ax[1].set_title('Debt of Federal Government during 1988-2010 ( % of GDP)')
    dataPlot['Debt of Federal Gov'].plot(
        linestyle='-', marker='*', color='r', ax=ax[1])
    plt.show()

    ##### Trend Model With  Federal Expenditure######
    dataPlot.reset_index(inplace=True)
    print(dataPlot.head())
    fedExpTrend = dataPlot.loc[:, 'date': 'Federal Military Expenditure']
    trend_model = LinearRegression(normalize=True, fit_intercept=True)
    trend_model.fit(np.array(fedExpTrend.index).reshape(
        (-1, 1)), fedExpTrend['Federal Military Expenditure'])
    print('Trend model coefficient={} and intercept={}'.format(
        trend_model.coef_[0], trend_model.intercept_))


def panelData(countries):
    wdi = WDI_api()
    data = pd.read_csv('indicators.csv')
    mExpCode = data[data.indicatorName ==
                    'Military expenditure (% of GDP)'].indicatorCode
    dataPlot = pd.DataFrame([])
    for i, country in enumerate(countries):
        df = dataPlot
        (info2, mExpData) = wdi.getData(country, mExpCode[9684])
        dataPlot = mExpData[['date', 'value']]
        dataPlot.set_index('date', inplace=True)
        dataPlot.dropna(inplace=True)
        try:
            dataPlot = pd.merge(dataPlot, df, on='date')
        except:
            pass
    plt.figure(figsize=(5.5, 5.5))
    dataPlot.plot()
    plt.legend(['USA', 'CHINA', 'UK', 'INDIA'], loc=1)
    plt.title('Miltitary expenditure of 5 countries over 10 years')
    plt.ylabel('Military expenditure (% of GDP)')
    plt.xlabel('Years')
    plt.show()


if __name__ == "__main__":
    #panelData(['usa', 'chn', 'gbr', 'ind'])
    usaTimeSeriesAnalysis()
