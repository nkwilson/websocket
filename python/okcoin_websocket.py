import websocket
import time
import sys
import json
import hashlib
import zlib
import base64

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
    finalStr = "{'event':'addChannel','channel':'ok_futuresusd_trade','parameters':{'api_key':'"+api_key+"',\
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
    return "{'event':'addChannel','channel':'ok_sub_futureusd_trades','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'},'binary':'true'}"

def on_ping(self):
    print ('ping recv')
    self.send("{'event':'pong'}")

def on_pong(self):
    print ('pong recv')
    self.send("{'event':'ping'}")

def on_open(self):
    #subscribe okcoin.com spot ticker
    #self.send("{'event':'addChannel','channel':'ok_sub_spot_eth_btc_ticker'}")

    #subscribe okcoin.com future this_week ticker
    #self.send("{'event':'addChannel','channel':'ok_sub_spot_bch_btc_ticker'}")



    # can't provide binary parameter
    # self.send("{'event':'addChannel','channel':'ok_sub_spot_eth_btc_kline_1min'}")
    # Returned Value Description
    # [time, open price, highest price, lowest price, close price, volume]
    # [string, string, string, string, string, string]

    # subscribe future kline
    self.send("{'event':'addChannel','channel':'ok_sub_futureusd_btc_kline_quarter_1min'}")
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
    #futureTradeMsg = futureTrade(api_key,secret_key,'btc_usd','this_week','','2','1','1','20')
    #self.send(futureTradeMsg)

    #future trade cancel
    #futureCancelOrderMsg = futureCancelOrder(api_key,secret_key,'btc_usd','65464','this_week')
    #self.send(futureCancelOrderMsg)

    #subscrbe future trades for self
    #futureRealTradesMsg = futureRealTrades(api_key,secret_key)
    #self.send(futureRealTradesMsg)
def on_message(self,evt):
    #print (evt) # just raw data, not compressed
    # target0=eval(evt)
    # print (target0)
    # target=target0[0]
    # print (target.keys(), target.values())
    target=eval(evt)[0]
    print (target['data'])
    # spec={"binary":"binary", "channel":"channel", "data":"data"}
    # print (spec.keys(), spec.values())
    # print (glom.glom(target, spec))  # already dict , no need of glom processing 
    #data = inflate(evt) #data decompress
    self.send("{'event':'ping'}")
    self.send("{'event':'pong'}")    

def inflate(data):
    print ('inflate', data)
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    print ('after decompress')
    inflated += decompress.flush()
    print (inflated)
    return inflated

def on_error(self,evt):
    print (evt)

def on_close(self):
    print ('DISCONNECT')

if __name__ == "__main__":
#    url = "wss://real.okcoin.com:10440/websocket/okcoinapi"      #if okcoin.cn  change url wss://real.okcoin.cn:10440/websocket/okcoinapi
#    api_key='your api_key which you apply'
#    secret_key = "your secret_key which you apply"

    url = "wss://real.okex.com:10440/websocket/okexapi"
    api_key = 'e2625f5d-6227-4cfd-9206-ffec43965dab'
    secret_key = "27BD16FD606625BCD4EE6DCA5A8459CE"
    
    websocket.enableTrace(False)
    if len(sys.argv) < 2:
        host = url
        print ('Run standalone')
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.on_ping = on_ping
    ws.on_pong = on_pong

    ws.ping_interval=28
    ws.ping_timeout=60

    ws.run_forever()
