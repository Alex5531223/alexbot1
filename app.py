import json, binance.client
from flask import Flask, request
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
symbol = 'BTCBUSD'
api_key = 'LrcoP5faLeT9qFJzdHPfMdimBrdK1un3b1YQgxR7Gjj0Vi2pVDo8jn3qto95itmG'
api_secret = 'hpumlCQ30lpsydMSPLZxkeQwgd96o5NMAFAGbDcdS3nytzxZaDiaDG2rkWpHKI8l'

# api_key = '12d15a558ea00f21a1526acdea6c34b12974deb44e3d2a66675c8c19a8188163'
# api_secret = 'fabdda6763a3a539ea316b9fb149e9711c6b04d933a826c28e1fee94351aa178'



client = Client(api_key, api_secret, testnet=False)


@app.route("/")
def helloworld():
    return 'hello world'


@app.route("/webhook", methods=["POST"])
def webhook():
    data = json.loads(request.data)

    EN_long = data["EN_long"]
    EN_short = data["EN_short"]
    STprice = data["ST"]
    TPprice = data["TP"]
    SIZE = data["SIZE"]
    LEV = 3
    orderID = data["orderID"]
    Direction = data["Direction"].upper()
    print(Direction)
    client.futures_change_leverage(symbol=symbol, leverage=3)

    def on_message(wsapp, message):
        print(message)

    if Direction == "BUY" and (orderID == "Enter_Long_Trend" or orderID == "Enter_Long_Hoffman"):
        client.futures_cancel_all_open_orders(symbol=symbol)

        buyorder = client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=SIZE)

        stoporder = client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=SIZE,stopPrice=STprice, reduceOnly=True)

        profitorder = client.futures_create_order(symbol=symbol, side='SELL', type='TRAILING_STOP_MARKET', quantity=SIZE,activationPrice=TPprice, callbackrate=0.1, reduceOnly=True)

    if Direction == "SELL" and (orderID == "Enter_Short_Trend" or orderID == "Enter_Short_Hoffman" or orderID == "Enter_Short_Hull" or orderID == "Enter_Short_TrendB"):
        client.futures_cancel_all_open_orders(symbol=symbol)

        sellorder = client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=SIZE)

        stoporder = client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=SIZE,
                                                stopPrice=STprice, reduceOnly=True)

        profitorder = client.futures_create_order(symbol=symbol, side='BUY', type='TRAILING_STOP_MARKET',
                                                  quantity=SIZE, activationPrice=TPprice, callbackrate=0.1, reduceOnly=True)

    return {
        "code": "success",
        "massage": data
    }


if __name__ == "__main__":
    app.run(debug=True)
