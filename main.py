import json
import keymanage  # get keys
import trade_api
import chbtc_api
def main():
    trade = trade_api.trade_api()
    wallet = chbtc_api.chbtc_api(str(keymanage.access_key),str(keymanage.secret_key))

    wallet.make_order("10","1","1","btc")
    pass


if __name__ == '__main__':
    main()
