import requests
import urllib3
import json
import os
import pandas as pd
import numpy as np


##################################
#
#   WDI_api is a class developed to
#   Handle requests and get data from
#   Word Bank api
#
##################################

class WDI_api:

    def __init__(self):
        self.Base_url = 'http://api.worldbank.org/v2/'
        self.Ind_url = 'indicator?format=json'
        self.http = urllib3.PoolManager()

    def getAllIndicators(self):
        r = self.http.request('GET', self.Base_url + self.Ind_url)
        parsed = json.loads(r.data)
        pages = parsed[0]['pages']
        data = {}
        indicators = []
        code = []
        for i in range(1, pages, 1):
            if i != 1:
                url = self.Base_url + self.Ind_url + "&page={}".format(i)
            else:
                url = self.Base_url + self.Ind_url
            r = self.http.request('GET', url)
            parsed = json.loads(r.data)
            listIndicators = parsed[1]
            data = {}
            for indicator in listIndicators:
                indicators.append(indicator['name'])
                code.append(indicator['id'])
        data['indicatorCode'] = code
        data['indicatorName'] = indicators
        frame = pd.DataFrame(data)
        frame.to_csv('indicators.csv')

    def IndicatorInfo(self, code):
        url = self.Base_url + 'indicators/{}?format=json'.format(code)
        r = self.http.request('GET', url)
        parsed = json.loads(r.data)
        data = {}
        attr = parsed[1][0]
        data['name'] = attr['name']
        data['unit'] = attr['unit']
        data['source'] = attr['source']['value']
        data['Description'] = attr['sourceNote']
        return data

    def getData(self, country, indCode, **kwargs):
        date = kwargs.get('date', None)
        if date == None:
            url = self.Base_url + 'country/' + country + \
                "/indicator/" + indCode + '?format=json'
        else:
            url = self.Base_url + 'country/' + country + "/indicator/" + \
                indCode + '?format=json' + '&date={}'.format(date)
        r = self.http.request('GET', url)
        parsed = json.loads(r.data)
        pages = parsed[0]['pages']
        frames1 = []
        frames2 = []
        for i in range(1, pages, 1):
            if i != 1:
                urlPages = url + "&page={}".format(i)
            else:
                urlPages = url
            r = self.http.request('GET', urlPages)
            parsed = json.loads(r.data)
            dfInfo = pd.json_normalize(parsed[0])
            dfData = pd.json_normalize(parsed[1])
            frames1.append(dfInfo)
            frames2.append(dfData)
        dfInfo = pd.concat(frames1)
        dfData = pd.concat(frames2)
        return dfInfo, dfData


if __name__ == "__main__":
    wdi = WDI_api()
    # wdi.getIndicators()
    # wdi.IndicatorInfo('5.1.2_KGZ.TOTA.AID.ADPP.GIZ')
    wdi.getData('all', 'DPANUSSPB', date='2010')
