
import keymanage  # get keys
import user
import time

def main():
    # trade = trade_api.trade_api()
    # wallet = chbtc_api.chbtc_api(str(keymanage.access_key),str(keymanage.secret_key))
    me = user.User(str(keymanage.access_key), str(keymanage.secret_key))
    print(me.getMoney())

    me.buyBTC(10.0, 0.001)
    time.sleep(10)
    buyList = me.getPendingBuyList()
    for bb in buyList:
        print(bb)
        me.cancelOrder(bb)
        time.sleep(10)
    # wallet.make_buy(10,1.0)
    # print(wallet.get_buy_list())
    # print(wallet.cancel_order(20160505251570460))
    pass


if __name__ == '__main__':
    main()
