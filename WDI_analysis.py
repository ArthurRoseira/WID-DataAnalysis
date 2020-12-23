import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from connect import WDI_api


if __name__ == "__main__":
    wdi = WDI_api()
    # wdi.getAllIndicators()

    ##### Getting Cross-Sectional Data ####
    data = pd.read_csv('indicators.csv')
    ind1Code = data[data.indicatorName ==
                    'Central government debt, total (% of GDP)'].indicatorCode
    ind2Code = data[data.indicatorName ==
                    'Military expenditure (% of GDP)'].indicatorCode
    (info1, data1) = wdi.getData(
        'all', ind1Code[6920], date='2010')
    (info2, data2) = wdi.getData('all', ind2Code[9684], date='2010')
    d1 = data1[['countryiso3code', 'value']]
    d2 = data2[['countryiso3code', 'value']]
    dataPlot = pd.merge(d1, d2, on='countryiso3code')
    dataPlot.columns = ['Country', 'central_govt_debt', 'military_exp']

    #### Plotting Cross-Sectional Data #####
    fig, axs = plt.subplots(ncols=2)
    graph1 = sns.histplot(data=dataPlot['military_exp'], ax=axs[0]).set_title(
        'Military expenditure (% of GDP) of 85 countries in 2010')
    graph2 = sns.kdeplot(data=dataPlot.central_govt_debt, ax=axs[1]).set_title(
        "Debt of central governments in 2010")
    plt.show()
