import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

# Reading DataBase
os.chdir(os.path.dirname(os.path.abspath(__file__)))
data = pd.read_csv('WDIData.csv')
#print('Column names:{}'.format(data.columns))
#print('Rows, Columns:{}'.format(data.shape))

# Selecting and Cleaning Data
# Unique Countries
# Shape return tuple of array dimensions
uniqueCountries = data['Country Code'].unique().shape[0]
#print('Number of Countries:{}'.format(uniqueCountries))
# Slicing data into New DataFrames
# Data Frame 1:  Total Central Government Debt (as % of GDP)
central_govt_debt = data.loc[data['Indicator Name']
                             == 'Central government debt, total (% of GDP)']
military_exp = data.loc[data['Indicator Name']
                        == 'Military expenditure (% of GDP)']
desc1 = central_govt_debt['2010'].describe()
desc2 = military_exp['2010'].describe()
print(desc1)
print(desc2)

# Setting Frame index
central_govt_debt.index = central_govt_debt['Country Code']
# Creating two series
central_govt_debt2010 = central_govt_debt['2010']
military_exp2010 = military_exp['2010']
print(military_exp2010.shape)
# Merging Data Frames
dataPlot = pd.concat((central_govt_debt2010, military_exp2010), axis=1)
dataPlot.columns = ['central_govt_debt', 'military_exp']
MilitaryPlot = dataPlot.loc[(dataPlot.military_exp.isnull() == False)]
# Taking only countries with both columns info
#### Plotting Cross-Sectional Data #####

fig, axs = plt.subplots(ncols=2)
graph1 = sns.histplot(data=MilitaryPlot['military_exp'], ax=axs[0]).set_title(
    'Military expenditure (% of GDP) of 85 countries in 2010')
graph2 = sns.kdeplot(data=dataPlot.central_govt_debt, ax=axs[1]).set_title(
    "Debt of central governments in 2010")
plt.show()
