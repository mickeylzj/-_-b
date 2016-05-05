import json
import urllib.request
import hashlib
import struct
import time
import sys


class chbtc_api:
    def __init__(self, mykey, mysecret):
        self.mykey = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in range(len(slist)):
            slist[index] = chr(slist[index] ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb = struct.pack("%ds" % len(aKey), aKey.encode())
        value = struct.pack("%ds" % len(aValue), aValue.encode())
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad.encode())
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad.encode())
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value = struct.pack("%ds" % len(aValue), aValue.encode())
        # print value
        h = hashlib.sha1()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params=''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time() * 1000)
            params += '&sign=%s&reqTime=%d' % (sign, reqTime)
            url = 'https://trade.chbtc.com/api/' + path + '?' + params
            # request = urllib.request(url)
            response = urllib.request.urlopen(url, timeout=2)
            doc = json.loads(response.read().decode())
            return doc
        except Exception as ex:
            # print >> sys.stderr, 'chbtc request ex: ', ex
            raise ex
            #  return None

    def get_account_info(self):
        # 返回值说明
        #
        # auth_google_enabled: 是否开通谷歌验证
        # auth_mobile_enabled: 是否开通手机验证
        # trade_password_enabled: 是否开通交易密码
        # username: 用户名
        # balance(余额):
        # CNY(人民币详情):
        # amount: 余额
        # currency: 币种
        # symbol: 货币符号（encodeURI编码）
        # BTC(比特币详情):
        # amount: 余额
        # currency: 币种
        # symbol: 货币符号（encodeURI编码）
        # BTC(莱特币详情):
        # amount: 余额
        # currency: 币种
        # symbol: 货币符号（encodeURI编码）
        # BTC(以太币详情):
        # amount: 余额
        # currency: 币种
        # symbol: 货币符号（encodeURI编码）
        # frozen(冻结):
        # CNY(人民币详情):
        # amount: 余额
        # currency: 币种
        # symbol: 货币符号（encodeURI编码）
        # BTC(比特币详情):
        # amount: 余额
        # currency: 币种
        # symbol: 货币符号（encodeURI编码）
        # BTC(莱特币详情):
        # amount: 余额
        # currency: 币种
        # symbol: 货币符号（encodeURI编码）
        # BTC(以太币详情):
        # amount: 余额
        # currency: 币种
        # symbol: 货币符号（encodeURI编码）
        # p2p:
        # inCNY(已借入人民币):
        # inBTC(已借入比特币):
        # inLTC(已借入莱特币):
        # inLTC(已借入以太币):
        # outCNY(已借出人民币):
        # outBTC(已借出比特币):
        # outLTC(已借出莱特币):
        # outLTC(已借出以太币):
        try:
            params = "method=getAccountInfo&accesskey=" + self.mykey
            path = 'getAccountInfo'

            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            sys.stderr.write('chbtc get_account_info exception,', ex)
            raise ex

    def __make_order(self, price, amount, tradeType, currency):
        # 返回值说明
        #
        # code: 返回代码
        # message: 提示信息
        # id: 委托挂单号
        try:
            params = "method=order&accesskey=" + self.mykey + "&price=" + price + \
                     "&amount=" + amount + "&tradeType=" + tradeType + "&currency=" + currency
            path = 'order'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            sys.stderr.write('chbtc make_order_api exception,', ex)
            raise ex
            # return None

    def make_buy(self, price: float, amount: float):
        return self.__make_order(str(price), str(amount), "1", "btc")

    def make_sell(self, price, amount):
        return self.__make_order(price, amount, "0", "btc")

    def get_order(self, id, currency='btc'):
        # 返回值说明
        #
        # currency: 交易类型（目前仅支持BTC / LTC / ETH）
        # id: 委托的挂单号
        # price: 单价
        # status: 挂单状态（0、待成交
        # 1、取消
        # 2、交易完成
        # 3、待成交未交易部份）
        # total_amount: 挂单总数量
        # trade_amount: 已成交数量
        # trade_date: Unix
        # 时间戳
        # trade_money: 已成交总金额
        # type: 挂单类型
        # 1 / 0[buy / sell]
        try:
            params = "method=getOrder&accesskey=" + self.mykey + "&id=" + id + \
                     "&currency=" + str(currency)
            path = 'getOrder'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            sys.stderr.write('chbtc get_order exception,', ex)
            raise ex
            # return None

    def __get_order_list(self, tradeType, currency, pageIndex: int = 1, pageSize: int = 100):
        # 返回值说明
        #
        # currency: 交易类型（目前仅支持BTC / LTC / ETH）
        # id: 委托的挂单号
        # price: 单价
        # status: 挂单状态（0、待成交
        # 1、取消
        # 2、交易完成
        # 3、待成交未交易部份）
        # total_amount: 挂单总数量
        # trade_amount: 已成交数量
        # trade_date: Unix
        # 时间戳
        # trade_money: 已成交总金额
        # type: 挂单类型
        # 1 / 0[buy / sell]
        try:
            params = "method=getOrdersNew&accesskey=" + self.mykey + "&tradeType=" + tradeType + \
                     "&currency=" + str(currency) + "&pageIndex=" + str(pageIndex) + "&pageSize=" + str(pageSize)
            path = 'getOrdersNew'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            sys.stderr.write('chbtc __get_order_list exception,', ex)
            raise ex
            # return None

    def get_buy_list(self, pageIndex: int = 1, pageSize: int = 100):
        return self.__get_order_list("1", "btc", pageIndex, pageSize)

    def get_sell_list(self, pageIndex: int = 1, pageSize: int = 100):
        return self.__get_order_list("0", "btc", pageIndex, pageSize)

    def get_order_list(self, currency: str = 'btc', pageIndex: int = 1, pageSize: int = 100):
        # 返回值说明
        #
        # currency: 交易类型（目前仅支持BTC / LTC / ETH）
        # id: 委托的挂单号
        # price: 单价
        # status: 挂单状态（0、待成交
        # 1、取消
        # 2、交易完成
        # 3、待成交未交易部份）
        # total_amount: 挂单总数量
        # trade_amount: 已成交数量
        # trade_date: Unix
        # 时间戳
        # trade_money: 已成交总金额
        # type: 挂单类型
        # 1 / 0[buy / sell]
        try:
            params = "method=getOrdersIgnoreTradeType&accesskey=" + self.mykey + \
                     "&currency=" + str(currency) + "&pageIndex=" + str(pageIndex) + "&pageSize=" + str(pageSize)
            path = 'getOrdersIgnoreTradeType'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            sys.stderr.write('chbtc get_order_list(IgnoreTradeType) exception,', ex)
            raise ex
            # return None

    def get_unfinished_order_list(self, currency: str = 'btc', pageIndex: int = 1, pageSize: int = 100):
        # 返回值说明
        #
        # currency: 交易类型（目前仅支持BTC / LTC / ETH）
        # id: 委托的挂单号
        # price: 单价
        # status: 挂单状态（0、待成交
        # 1、取消
        # 2、交易完成
        # 3、待成交未交易部份）
        # total_amount: 挂单总数量
        # trade_amount: 已成交数量
        # trade_date: Unix
        # 时间戳
        # trade_money: 已成交总金额
        # type: 挂单类型
        # 1 / 0[buy / sell]
        try:
            params = "method=getUnfinishedOrdersIgnoreTradeType&accesskey=" + self.mykey + \
                     "&currency=" + str(currency) + "&pageIndex=" + str(pageIndex) + "&pageSize=" + str(pageSize)
            path = 'getUnfinishedOrdersIgnoreTradeType'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            sys.stderr.write('chbtc get_unfinished_order_list exception,', ex)
            raise ex
            # return None

    def cancel_order(self, id, currency: str = 'btc'):
        # 返回值说明
        #
        # code: 返回代码
        # message: 提示信息
        try:
            params = "method=cancelOrder&accesskey=" + self.mykey + "&id=" + str(id) + \
                     "&currency=" + str(currency)
            path = 'cancelOrder'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            sys.stderr.write('chbtc cancel_order exception,', ex)
            raise ex
            # return None

#
# if __name__ == '__main__':
#     access_key = 'accesskey'
#     access_secret = 'secretkey'
#
#     api = chbtc_api(access_key, access_secret)
#
#     print api.query_account()
