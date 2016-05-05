import chbtc_api
import threading
import time
import log
import sys

logger = log.logger()


# class _Order:
#     def __init__(self, id, price, status, total_amount, trade_amount, trade_date, trade_money, type):
#         self.id = id
#         self.price = price
#         self.status = status
#         self.total_amount = total_amount
#         self.trade_amount = trade_amount
#         self.trade_date = trade_date
#         self.trade_money = trade_money
#         self.type = type


class User:
    def __init__(self, access_key, secret_key):
        self._cny = 0.0  # 账户人民币可用余额
        self._btc = 0.0  # 账户比特币可用余额
        self._buyList = {}  # 买单列表
        self._sellList = {}  # 卖单列表
        self._pendingBuyList = {}  # 等待成交的买单列表
        self._pendingSellList = {}  # 等待成交的卖单列表
        self._api = chbtc_api.chbtc_api(access_key, secret_key)  # 操作交易的api

        # 初始化时，加载3页已完成的order
        for i in range(1, 4):
            try:
                self._refreshSell(page=i)
                time.sleep(0.1)
                self._refreshBuy(page=i)
                time.sleep(0.1)
            except Exception as e:
                print(e,"\n初始化时发生网络故障,请重新启动程序",file=sys.stderr)
                exit()

        print(self._buyList)
        self._refreshThread = []  # 刷新的线程池
        t1 = threading.Thread(target=self._refreshWalletThread)
        self._refreshThread.append(t1)
        t1.start()
        t2 = threading.Thread(target=self._refreshPendingListThread)
        self._refreshThread.append(t2)
        t2.start()
        t3 = threading.Thread(target=self._refreshCompleteOrderThread)
        self._refreshThread.append(t3)
        t3.start()

    def _refreshCompleteOrderThread(self):
        while True:
            try:
                self._refreshBuy()
                self._refreshSell()
                time.sleep(1)
            except Exception as ex:
                print("[ERROR] refresh complete orders failed.", ex, file=sys.stderr)

    def _refreshBuy(self, page: int = 1):
        result = self._api.get_buy_list(pageIndex=page)
        if result is not None:
            if 'code' not in result or result['code'] == 1000:
                for buy in result:
                    if (buy['type'] == 1 and buy['status'] == 2):  # 买入委托，且交易已成功
                        if buy['id'] not in self._buyList:
                            self._buyList[buy['id']] = buy
                pass
            else:
                print("get_buy_list error", result['code'], result['message'], file=sys.stderr)

        else:
            print("get_buy_list error, None.", file=sys.stderr)

    def _refreshSell(self, page: int = 1):
        # for page in range()
        result = self._api.get_sell_list(pageIndex=page)
        if result is not None:
            if 'code' not in result or result['code'] == 1000:
                for sell in result:
                    if (sell['type'] == 0 and sell['status'] == 2):  # 买入委托，且交易已成功
                        if sell['id'] not in self._sellList:
                            self._sellList[sell['id']] = sell
                pass
            else:
                print("get_sell_list error", result['code'], result['message'], file=sys.stderr)

        else:
            print("get_sell_list error, None.", file=sys.stderr)

    def _refreshWalletThread(self):  # 开始刷新我钱包内余额
        while True:
            try:
                self._refreshWallet()
                time.sleep(1)
            except Exception as ex:
                print("[ERROR] refresh wallet failed.", ex, file=sys.stderr)

    def _refreshWallet(self):  # 刷新钱包内的余额
        result = self._api.get_account_info()
        # print(result)
        if result is not None:
            if not hasattr(result, 'code') or result['code'] == 1000:
                # 成功
                self._cny = result['result']['balance']['CNY']['amount'] - result['result']['frozen']['CNY']['amount']
                self._btc = result['result']['balance']['BTC']['amount'] - result['result']['frozen']['BTC']['amount']
                pass
            else:
                print("get_account_info error", result['code'], result['message'], file=sys.stderr)

        else:
            print("get_account_info error, None.", file=sys.stderr)

    def _refreshPendingListThread(self):  # 开始刷新等待成交的单子
        while True:
            try:
                self._refreshPendingList()
                time.sleep(1)
            except Exception as ex:
                print("[ERROR] refresh pending list failed.", ex, file=sys.stderr)
                raise ex

    def _refreshPendingList(self):  # 刷新等待成交的单子
        result = self._api.get_unfinished_order_list()
        pendingIdList = []
        if result is not None:
            if (('code' not in result) or result['code'] == 1000):
                # 成功
                for order in result:
                    if order['type'] == 0:  # 卖单
                        # id, price, status, total_amount, trade_amount, trade_date, trade_money, type
                        orderId = str(order['id'])
                        pendingIdList.append(orderId)
                        self._pendingSellList[orderId] = {}
                        self._pendingSellList[orderId]['status'] = order['status']
                        self._pendingSellList[orderId]['trade_amount'] = order['trade_amount']
                        self._pendingSellList[orderId]['trade_date'] = order['trade_date']
                        self._pendingSellList[orderId]['trade_money'] = order['trade_money']
                        pass
                    elif order['type'] == 1:  # 买单
                        orderId = str(order['id'])
                        pendingIdList.append(orderId)
                        self._pendingBuyList[orderId] = {}
                        self._pendingBuyList[orderId]['status'] = order['status']
                        self._pendingBuyList[orderId]['trade_amount'] = order['trade_amount']
                        self._pendingBuyList[orderId]['trade_date'] = order['trade_date']
                        self._pendingBuyList[orderId]['trade_money'] = order['trade_money']
                        pass
                for id in list(self._pendingBuyList.keys()):
                    if id not in pendingIdList:  # 说明已经成交或取消
                        self._pendingBuyList.pop(id)
                        pass
                for id in list(self._pendingSellList.keys()):
                    if id not in pendingIdList:  # 说明已经成交或取消
                        self._pendingSellList.pop(id)
                        pass

                pass
            elif result['code'] == 3001:  # 没有单子
                pass
            else:
                print("get_unfinished_order_list error", result['code'], result['message'], file=sys.stderr)

        else:
            print("get_unfinished_order_list error, None.", file=sys.stderr)

    def getMoney(self):  # 获取钱包信息
        self._refreshWallet()
        return {'cny': self._cny, 'btc': self._btc}

    def buyBTC(self, price: float = 1.0, amount: float = 0.001):  # 委托买进比特币
        result = self._api.make_buy(price=price, amount=amount)
        # print(result)
        if result is not None:
            if not hasattr(result, 'code') or result['code'] == 1000:
                # 成功
                orderId = result['id']
                self._pendingBuyList[orderId] = {'id': orderId, 'price': price, 'status': 0, 'total_amount': amount,
                                                 'trade_amount': 0.0, 'trade_date': 0, 'trade_money': 0, 'type': 1}
                logger.write("SUCCESS\tbuy\t%s\t%f\t%f" % (orderId, price, amount))
                pass
            else:
                print("make_buy error", result['code'], result['message'], file=sys.stderr)
                logger.write("FAIL\tbuy\t%d\t%s" % (result['code'], result['message']))

        else:
            print("make_buy error, None.", file=sys.stderr)
            logger.write("FAIL\tbuy\tNone")

    def sellBTC(self, price: float = 500000, amount: float = 0.001):  # 委托卖出比特币
        result = self._api.make_sell(price=price, amount=amount)
        # print(result)
        if result is not None:
            if not hasattr(result, 'code') or result['code'] == 1000:
                # 成功
                orderId = result['id']
                self._pendingSellList[orderId] = {'id': orderId, 'price': price, 'status': 0, 'total_amount': amount,
                                                  'trade_amount': 0.0, 'trade_date': 0, 'trade_money': 0, 'type': 1}
                logger.write("SUCCESS\tsell\t%s\t%f\t%f" % (orderId, price, amount))
                pass
            else:
                print("make_sell error", result['code'], result['message'], file=sys.stderr)
                logger.write("FAIL\tsell\t%d\t%s" % (result['code'], result['message']))

        else:
            print("make_sell error, None.", file=sys.stderr)
            logger.write("FAIL\tsell\tNone")

    def cancelOrder(self, id):
        result = self._api.cancel_order(id)
        if result is not None:
            if not hasattr(result, 'code') or result['code'] == 1000:
                # 成功
                logger.write("SUCCESS\tcancel\t%s" % (id))
                pass
            else:
                print("make_sell error", result['code'], result['message'], file=sys.stderr)
                logger.write("FAIL\tcancel\t%d\t%s" % (result['code'], result['message']))

        else:
            print("make_sell error, None.", file=sys.stderr)
            logger.write("FAIL\tcancel\tNone")

    def getPendingBuyList(self):  # 获取正在委托买入的单子
        return self._pendingBuyList.copy()

    def getPendingSellList(self):  # 获取正在委托卖出的单子
        return self._pendingSellList.copy()
    def getBuyList(self): # 获得购买成功的单子
        return  self._buyList.copy()
    def getSellList(self):# 获得卖出成功的单子
        return  self._sellList.copy()
