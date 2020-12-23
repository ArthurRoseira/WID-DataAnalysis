import requests
import urllib3
import json
from xml.etree import ElementTree


class WDI_api:

    def __init__(self):
        self.Base_url = 'http://api.worldbank.org/v2/'
        self.Ind_url = 'indicator?format=json'
        self.http = urllib3.PoolManager()

    def getIndicators(self):
        r = self.http.request('GET', self.Base_url + self.Ind_url)
        parsed = json.loads(r.data)
        pages = parsed[0]['pages']
        for i in range(1, pages, 1):
            if i != 1:
                url = self.Base_url + self.Ind_url + "&page={}".format(i)
            else:
                url = self.Base_url + self.Ind_url
            r = self.http.request('GET', url)
            parsed = json.loads(r.data)
            listIndicators = parsed[1]
            for indicator in listIndicators:
                print(indicator['name'])


if __name__ == "__main__":
    wdi = WDI_api()
    wdi.getIndicators()
