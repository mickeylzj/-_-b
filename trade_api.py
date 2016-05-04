import json, urllib2, hashlib, struct, sha, time, sys


class trade_api:
    def __init__(self):
        pass

    def get_ticker(self):
        try:
            url = 'http://api.chbtc.com/data/ticker'
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception, ex:
            print >> sys.stderr, 'chbtc get_ticker error: ', ex
            return None

    def get_depth(self):
        try:
            url = 'http://api.chbtc.com/data/depth'
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception, ex:
            print >> sys.stderr, 'chbtc get_depth error: ', ex
            return None

    def get_trades(self, since=None):
        try:
            print since
            url = 'http://api.chbtc.com/data/depth'
            if since is not None:
                url = url + "?since=" + since
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception, ex:
            print >> sys.stderr, 'chbtc get_depth error: ', ex
            return None
