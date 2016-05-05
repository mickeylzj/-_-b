import json, urllib, hashlib, struct, time, sys


class trade_api:
    def __init__(self):
        pass

    def get_ticker(self):
        try:
            url = 'http://api.chbtc.com/data/ticker'
            request = urllib.Request(url)
            response = urllib.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception as ex:

            sys.stderr.write('chbtc get_ticker error\n')
            raise ex

    def get_depth(self):
        try:
            url = 'http://api.chbtc.com/data/depth'
            request = urllib.Request(url)
            response = urllib.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception as ex:
            sys.stderr.write('chbtc get_depth error\n')
            raise ex

    def get_trades(self, since=None):
        try:
            # print since
            url = 'http://api.chbtc.com/data/depth'
            if since is not None:
                url = url + "?since=" + since
            request = urllib.Request(url)
            response = urllib.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception as ex:
            sys.stderr.write('chbtc get_depth error\n')
            raise ex
