import json, binance.client
from flask import Flask, request
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
symbol = 'BTCBUSD'
api_key = 'kZGgziDenC8TFJIXxJZ4gY77Q2B0nVrQiC3PLftLpLns8pjDiyRLZQrgHSebr5Ds'
api_secret = 'LTmwFOBobewVvLHJJymspPp5RuiNo8bMPXsKkLBXIYfZRbWQZLegTH6T4Nnk44lf'


client = Client(api_key, api_secret, testnet=True)

@app.route("/")
def helloworld():
    return 'hello world'

@app.route("/webhook", methods=["POST"])
def webhook():
    data = json.loads(request.data)
    # order_open_symbol =client.futures_account()['positions'][14]['positionAmt']
    # print(order_open_symbol)

    EN_long=data["EN_long"]
    EN_short = data["EN_short"]
    STprice=data["ST"]
    TPprice=data["TP"]
    SIZE=0.001
    LEV= 3
    orderID=data["orderID"]
    Direction=data["Direction"].upper()
    print(Direction)
    #Position_size=data["strategypositionsize"]
    client.futures_change_leverage(symbol=symbol, leverage=3)

    def on_message(wsapp, message):
        print(message)

    # wsapp = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcbusd@kline_<im>", on_message=on_message)
    # print(wsapp)
    # wsapp.run_forever()

    if Direction=="BUY"  and (orderID=="Enter_Long_Trend"):


        client.futures_cancel_all_open_orders(symbol=symbol)

        buyorder = client.futures_create_order(symbol=symbol, side='BUY', type='LIMIT', quantity=SIZE, price=EN_long, timeInForce='GTC')

        stoporder = client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='SELL', type='LIMIT', quantity=SIZE, price=TPprice, timeInForce='GTC')#, postOnly=True)


    if Direction=="SELL"  and (orderID=="Enter_Short_Trend"):


        client.futures_cancel_all_open_orders(symbol=symbol)

        buyorder = client.futures_create_order(symbol=symbol, side='SELL', type='LIMIT', quantity=SIZE, price=EN_short, timeInForce='GTC')

        stoporder = client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='BUY', type='LIMIT', quantity=SIZE, price=TPprice, timeInForce='GTC')#, postOnly=True)

    return {
        "code": "success",
        "massage": data
    }

if __name__ == "__main__":
    app.run(debug=True)
