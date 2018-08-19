import json
import urllib.request

with urllib.request.urlopen("http://www.python.org") as url:
    s = url.read()


class ForexDataClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_uri = 'http://forex.1forge.com/1.0.2/'

    def fetch(self, uri):
        response = []
        with urllib.request.urlopen(self.base_uri + uri + '&api_key=' + self.api_key) as url:
            response = url.read()
        return json.loads(response)

    def quota(self):
        return self.fetch('quota?cache=false')

    def getSymbols(self):
        return self.fetch('symbols?cache=false')

    def getQuotes(self, pairs):
        return self.fetch('quotes?pairs=' + ','.join(pairs))

    def marketIsOpen(self):
        data = self.fetch('market_status?cache=false')
        try:
            return data['market_is_open']
        except:
            print(data)

    def convert(self, currency_from, currency_to, quantity):
        return self.fetch('convert?from=' + currency_from + '&to=' + currency_to + '&quantity=' + str(quantity))
