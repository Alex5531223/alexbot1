import json
from flask import Flask, request
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
symbol = 'BTCBUSD'
api_key = 'beUKPB5PA5CPmuE4OvCdW16iQJkL6ZzpfUc6uQEzCv9gsHZxIazCzGA2cpxBqOuy'
api_secret = 'NcUIjv55zeaZTfSYWNZwqwyyYvaJ0CPMFNTUgppVyz2EyfIrRdT5pTiC7ZXAydfr'
client = Client(api_key, api_secret, testnet=False)

@app.route("/")
def helloworld():
    return 'hello world'

@app.route("/webhook", methods=["POST"])
def webhook():
    data = json.loads(request.data)
    #print(data['bar']["open"])
    Etryprice=data["EN"]
    STprice=data["ST"]
    TPprice=data["TP"]
    SIZE=0.001
    LEVERAGE = data["LEV"]
    orederID=data["orderID"]
    Position_size=data["position_size"]
    #print(LEVERAGE)
    client.futures_change_leverage(symbol=symbol, leverage=1)
    aaa=client.futures_symbol_ticker(symbol=symbol)
    print(aaa)
    client.futures_cancel_all_open_orders(symbol=symbol)
    #client.future_can

    if orederID=="BUY" and Position_size=="0":

        buyorder = client.futures_create_order(symbol=symbol, side='BUY', type='STOP', quantity=SIZE, price=Etryprice, stopPrice=Etryprice, timeInForce='GTC')

        stoporder = client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='SELL', type='TAKE_PROFIT', quantity=SIZE, price=TPprice, stopPrice=TPprice)

    if orederID=="SELL" and Position_size=="0":

        buyorder = client.futures_create_order(symbol=symbol, side='SELL', type='STOP', quantity=SIZE, price=Etryprice,stopPrice=Etryprice,timeInForce='GTC')

        stoporder = client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='BUY', type='TAKE_PROFIT', quantity=SIZE, price=TPprice, stopPrice=TPprice)


    #print(Position_size)
    #print(data["strategy"]["order_action"])
    return {
        "code": "success",
        "massage": data
    }

if __name__ == "__main__":
    app.run(debug=True)
