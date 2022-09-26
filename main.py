import json
from flask import Flask, request
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
symbol = 'BTCBUSD'
api_key = '12d15a558ea00f21a1526acdea6c34b12974deb44e3d2a66675c8c19a8188163'
api_secret = 'fabdda6763a3a539ea316b9fb149e9711c6b04d933a826c28e1fee94351aa178'
client = Client(api_key, api_secret, testnet=True)

@app.route("/")
def helloworld():
    return 'hello world'

@app.route("/webhook", methods=["POST"])
def webhook():
    data = json.loads(request.data)
    client.futures_cancel_all_open_orders(symbol=symbol)
    Etryprice=data["EN"]
    STprice=data["ST"]
    TPprice=data["TP"]
    SIZE=data["SIZE"]
    LEV= 3
    orderID=data["orderID"]
    Direction=data["Direction"].upper()
    print(Direction)
    Position_size=data["strategypositionsize"]
    client.futures_change_leverage(symbol=symbol, leverage=1)



    if Direction=="BUY" and Position_size=="1" and (orderID=="Enter_Long_Trend"):


        buyorder = client.futures_create_order(symbol=symbol, side='BUY', type='LIMIT', quantity=SIZE, price=Etryprice, timeInForce='GTC')

        stoporder = client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='SELL', type='TAKE_PROFIT', quantity=SIZE, price=TPprice, stopPrice=TPprice)



    if Direction=="SELL" and Position_size=="-1" and (orderID=="Enter_Short_Trend"):

        buyorder = client.futures_create_order(symbol=symbol, side='SELL', type='LIMIT', quantity=SIZE, price=Etryprice, timeInForce='GTC')

        stoporder = client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='BUY', type='TAKE_PROFIT', quantity=SIZE, price=TPprice, stopPrice=TPprice)


    return {
        "code": "success",
        "massage": data
    }

if __name__ == "__main__":
    app.run(debug=True)
