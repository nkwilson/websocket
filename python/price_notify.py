import websocket
import time
import sys
import json
import hashlib
import zlib
import base64
import os
# import glom

api_key=''
secret_key = ""
#business
def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    return  hashlib.md5((sign+'secret_key='+secretKey).encode("utf-8")).hexdigest().upper()
#spot trade
def spotTrade(channel,api_key,secretkey,symbol,tradeType,price='',amount=''):
    params={
      'api_key':api_key,
      'symbol':symbol,
      'type':tradeType
     }
    if price:
        params['price'] = price
    if amount:
        params['amount'] = amount
    sign = buildMySign(params,secretkey)
    finalStr =  "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"',\
                'sign':'"+sign+"','symbol':'"+symbol+"','type':'"+tradeType+"'"
    if price:
        finalStr += ",'price':'"+price+"'"
    if amount:
        finalStr += ",'amount':'"+amount+"'"
    finalStr+="},'binary':'true'}"
    return finalStr

#spot cancel order
def spotCancelOrder(channel,api_key,secretkey,symbol,orderId):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'order_id':orderId
    }
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"','symbol':'"+symbol+"','order_id':'"+orderId+"'},'binary':'true'}"

#subscribe trades for self
def realtrades(channel,api_key,secretkey):
   params={'api_key':api_key}
   sign=buildMySign(params,secretkey)
   return "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'},'binary':'true'}"

# trade for future
# 28/07/2018, ok_futuresusd_trade/ok_sub_futureusd_btc_trade_quarter is not valid channel
def futureTrade(api_key,secretkey,symbol,contractType,price='',amount='',tradeType='',matchPrice='',leverRate=''):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'contract_type':contractType,
      'amount':amount,
      'type':tradeType,
      'match_price':matchPrice,
      'lever_rate':leverRate
    }
    if price:
        params['price'] = price
    sign = buildMySign(params,secretkey)
    
    # finalStr = "{'event':'addChannel','channel':'ok_futuresusd_trade','parameters':{'api_key':'"+api_key+"',\
    finalStr = "{'event':'addChannel','channel':'ok_sub_futureusd_btc_trade_quarter','parameters':{'api_key':'"+api_key+"',\
               'sign':'"+sign+"','symbol':'"+symbol+"','contract_type':'"+contractType+"'"
    if price:
        finalStr += ",'price':'"+price+"'"
    finalStr += ",'amount':'"+amount+"','type':'"+tradeType+"','match_price':'"+matchPrice+"','lever_rate':'"+leverRate+"'},'binary':'true'}"
    return finalStr

#future trade cancel
def futureCancelOrder(api_key,secretkey,symbol,orderId,contractType):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'order_id':orderId,
      'contract_type':contractType
    }
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'ok_futuresusd_cancel_order','parameters':{'api_key':'"+api_key+"',\
            'sign':'"+sign+"','symbol':'"+symbol+"','contract_type':'"+contractType+"','order_id':'"+orderId+"'},'binary':'true'}"

#subscribe future trades for self
def futureRealTrades(api_key,secretkey):
    params = {'api_key':api_key}
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'ok_sub_futureusd_trades','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'}}"

# subscrbe future user info, with userful info return
def futureUserInfo(api_key, secretkey):
    params = {'api_key':api_key}
    sign = buildMySign(params, secretkey)
    return "{'event':'addChannel','channel':'ok_futureusd_userinfo','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'}}"

# subscrbe future user info, no userful info return
def futureUserInfo2(api_key, secretkey):
    params = {'api_key':api_key}
    sign = buildMySign(params, secretkey)
    return "{'event':'addChannel','channel':'ok_sub_futureusd_userinfo','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'}}"

def on_ping(self, evt):
    print ('ping recv')
    self.send("{'event':'pong'}")

def on_pong(self, evt):
    print ('pong recv')
    self.send("{'event':'ping'}")

def on_open(self):
    global options
    #subscribe okcoin.com spot ticker
    #self.send("{'event':'addChannel','channel':'ok_sub_spot_eth_btc_ticker'}")

    #subscribe okcoin.com future this_week ticker
    #self.send("{'event':'addChannel','channel':'ok_sub_spot_bch_btc_ticker'}")

    # can't provide binary parameter
    # self.send("{'event':'addChannel','channel':'ok_sub_spot_eth_btc_kline_1min'}")
    # Returned Value Description
    # [time, open price, highest price, lowest price, close price, volume]
    # [string, string, string, string, string, string]

    # subscribe future kline 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 12hour, day, 3day, week
    if 'btc' in options.coin:
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_1min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_5min'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_15min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_30min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_1hour'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_2hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_4hour'}")    
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_6hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_12hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_day'}")

    if 'ltc' in options.coin:
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_1min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_5min'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_15min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_30min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_1hour'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_2hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_4hour'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_6hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_12hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_kline_quarter_day'}")

    if 'bch' in options.coin:
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_1min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_5min'}")    
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_15min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_30min'}")        
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_1hour'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_2hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_4hour'}")    
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_6hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_12hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bch_kline_quarter_day'}")

    if 'bsv' in options.coin:
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_1min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_5min'}")    
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_15min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_30min'}")        
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_1hour'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_2hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_4hour'}")    
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_6hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_12hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_bsv_kline_quarter_day'}")

    if 'eth' in options.coin:
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_1min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_5min'}")    
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_15min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_30min'}")        
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_1hour'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_2hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_4hour'}")    
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_6hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_12hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_kline_quarter_day'}")

    if 'eos' in options.coin:
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_1min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_5min'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_15min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_30min'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_1hour'}")
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_2hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_4hour'}")    
        #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_6hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_12hour'}")
        self.send("{'event':'addChannel','channel':'ok_sub_futureusd_eos_kline_quarter_day'}")
        
    #subscribe okcoin.com future depth
    #self.send("{'event':'addChannel','channel':'ok_sub_futureusd_ltc_depth_next_week_20','binary':'true'}")

    #subscrib real trades for self
    # realtradesMsg = realtrades('ok_sub_futureusd_btc_kline_quarter_1min',api_key,secret_key)
    # self.send(realtradesMsg)


    #spot trade via websocket
    #spotTradeMsg = spotTrade('ok_spotusd_trade',api_key,secret_key,'ltc_usd','buy_market','1','')
    #self.send(spotTradeMsg)


    #spot trade cancel
    #spotCancelOrderMsg = spotCancelOrder('ok_spotusd_cancel_order',api_key,secret_key,'btc_usd','125433027')
    #self.send(spotCancelOrderMsg)

    #future trade
    #futureTradeMsg = futureTrade(api_key,secret_key,'btc_usd','quarter','','2','1','1','10')
    #self.send(futureTradeMsg)

    #future trade cancel
    #futureCancelOrderMsg = futureCancelOrder(api_key,secret_key,'btc_usd','65464','this_week')
    #self.send(futureCancelOrderMsg)

    #subscrbe future trades for self
    #futureRealTradesMsg = futureRealTrades(api_key,secret_key)
    #self.send(futureRealTradesMsg)

    # subscrbe future user info
    #futureUserInfoMsg = futureUserInfo(api_key, secret_key)
    #futureUserInfoMsg = futureUserInfo2(api_key, secret_key)
    #self.send(futureUserInfoMsg)

price_notify_suffix = '.price_notify'
def on_message(self,evt):
    evt = inflate(evt).decode() #data decompress
    #print (evt, type(t)) # just raw data, not compressed
    target=eval(evt) # convert str to its real type
    if isinstance(target, dict):
        next_ticker=0
        return

    #print (target, type(target), type(target[0]))
    channel=target[0]['channel']
    data=target[0]['data'][0] # get list type of data
    print (channel.ljust(48), data[0]) # show every message
    if os.path.isdir(channel) == False:
        os.makedirs(channel, exist_ok=True)
    price_filename = os.path.join(os.getcwd(), channel, data[0])
    #print (price_filename)
    with open(price_filename, 'w') as f:
        f.write(str(data[1:])[1:-1] +"\n")
        f.close()
    # send out price notify signal
    price_notify_filename = os.path.join(os.getcwd(), '%s%s' % (channel, price_notify_suffix))
    #print (price_notify_filename)
    with open(price_notify_filename, 'w') as f:
        f.write(price_filename)
        f.close()
    # spec={"binary":"binary", "channel":"channel", "data":"data"}
    # print (spec.keys(), spec.values())
    # print (glom.glom(target, spec))  # already dict , no need of glom processing 
    #data = inflate(evt) #data decompress

def inflate(data):
    #print ('inflate', data)
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    #print ('after decompress')
    inflated += decompress.flush()
    #print (inflated)
    return inflated

def on_error(self,evt):
    print (evt)

def on_close(self):
    print ('DISCONNECT')

if __name__ == "__main__":
    global options
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('', '--coin', dest='coin', default=[],
                      action='append',
                      help='specify coin listener')
    (options, args) = parser.parse_args()
    print (type(options), options, args)
    if options.coin == '':
        options.coin = ['btc', 'eth', 'ltc']
#    url = "wss://real.okcoin.com:10440/websocket/okcoinapi"      #if okcoin.cn  change url wss://real.okcoin.cn:10440/websocket/okcoinapi
#    api_key='your api_key which you apply'
#    secret_key = "your secret_key which you apply"

    url = "wss://real.okex.com:10440/websocket/okexapi"
    api_key = 'e2625f5d-6227-4cfd-9206-ffec43965dab'
    secret_key = "27BD16FD606625BCD4EE6DCA5A8459CE"
    
    websocket.enableTrace(False)
    host = url
    
    # run for ever 
    while True:
        ws = websocket.WebSocketApp(url,
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close)
        ws.on_open = on_open
        ws.on_ping = on_ping
        ws.on_pong = on_pong
        
        ws.ping_interval=28
        ws.ping_timeout=60
        
        ws.run_forever(ping_interval=30, ping_timeout=60)
