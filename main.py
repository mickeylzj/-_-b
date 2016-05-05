import json
import keymanage  # get keys
import trade_api
import chbtc_api
def main():
    trade = trade_api.trade_api()
    wallet = chbtc_api.chbtc_api(str(keymanage.access_key),str(keymanage.secret_key))

    # wallet.make_buy(10,1.0)
    print(wallet.get_buy_list())
    print(wallet.cancel_order(20160505251570460))
    pass


if __name__ == '__main__':
    main()
