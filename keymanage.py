import json

access_key = ''
secret_key = ''
path = "./.key/key"
with open(path) as f:
    a = json.loads(f.read())
    # print( a)
    access_key=a['CHBTC_ACCESS_KEY']
    secret_key=a['CHBTC_SECRET_KEY']
