import json, binance.client
from flask import Flask, request
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
symbol = 'BTCBUSD'
api_key = 'kZGgziDenC8TFJIXxJZ4gY77Q2B0nVrQiC3PLftLpLns8pjDiyRLZQrgHSebr5Ds'
api_secret = 'LTmwFOBobewVvLHJJymspPp5RuiNo8bMPXsKkLBXIYfZRbWQZLegTH6T4Nnk44lf'

# api_key = '12d15a558ea00f21a1526acdea6c34b12974deb44e3d2a66675c8c19a8188163'
# api_secret = 'fabdda6763a3a539ea316b9fb149e9711c6b04d933a826c28e1fee94351aa178'

client = Client(api_key, api_secret, testnet=False)

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
    SIZE=data["SIZE"]
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

    if Direction=="BUY"  and (orderID=="Enter_Long_Trend" or orderID=="Enter_Long_Hoffman" ):


        client.futures_cancel_all_open_orders(symbol=symbol)

        buyorder = client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=SIZE, stopPrice=EN_long)

        stoporder = client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='SELL', type='LIMIT', quantity=SIZE, price=TPprice, timeInForce='GTC', postOnly=True)


    if Direction=="SELL"  and (orderID=="Enter_Short_Trend" or orderID=="Enter_Short_Hoffman" or orderID=="Enter_Short_Hull" or orderID=="Enter_Short_TrendB"):


        client.futures_cancel_all_open_orders(symbol=symbol)

        buyorder = client.futures_create_order(symbol=symbol, side='SELL', type='STOP_MARKET', quantity=SIZE, stopPrice=EN_short)

        stoporder = client.futures_create_order(symbol=symbol, side='BUY', type='STOP_MARKET', quantity=SIZE, stopPrice=STprice)

        profitorder = client.futures_create_order(symbol=symbol, side='BUY', type='LIMIT', quantity=SIZE, price=TPprice, timeInForce='GTC', postOnly=True)

    return {
        "code": "success",
        "massage": data
    }

if __name__ == "__main__":
    app.run(debug=True)
