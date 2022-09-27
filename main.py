import json
from flask import Flask, request
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
symbol = 'BTCBUSD'
api_key = 'FeQRkHLOp6U0rlaVSz4nhdqwGXKHUh2CWt7tMr7SZ2WYmFobCLn8QECC1cDIXxDm'
api_secret = 'SkuqJrk1Jg1FNWsaxIVTmfB3QDqvDVJxZnga71572EnhHjHjzfn9Ngy6W2DO2uhq'
client = Client(api_key, api_secret, testnet=False)

@app.route("/")
def helloworld():
    return 'hello world'

@app.route("/webhook", methods=["POST"])
def webhook():
    data = json.loads(request.data)

    Etryprice=data["EN"]
    STprice=data["ST"]
    TPprice=data["TP"]
    SIZE=0.001
    LEV= 3
    orderID=data["orderID"]
    Direction=data["Direction"].upper()
    print(Direction)
    Position_size=data["strategypositionsize"]
    client.futures_change_leverage(symbol=symbol, leverage=3)



    if Direction=="BUY"  and (orderID=="Enter_Long_Trend"):

        client.futures_cancel_all_open_orders(symbol=symbol)

        buyorder = client.futures_create_order(symbol=symbol, side='BUY', type='LIMIT', quantity=SIZE, price=Etryprice, timeInForce='GTC')

        stoporder = client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='SELL', type='TAKE_PROFIT', quantity=SIZE, price=TPprice, stopPrice=TPprice)



    if Direction=="SELL"  and (orderID=="Enter_Short_Trend"):


        client.futures_cancel_all_open_orders(symbol=symbol)

        buyorder = client.futures_create_order(symbol=symbol, side='SELL', type='LIMIT', quantity=SIZE, price=Etryprice, timeInForce='GTC')

        stoporder = client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='BUY', type='TAKE_PROFIT', quantity=SIZE, price=TPprice, stopPrice=TPprice)


    return {
        "code": "success",
        "massage": data
    }

if __name__ == "__main__":
    app.run(debug=True)
