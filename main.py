from binance.client import Client
api_key = '12d15a558ea00f21a1526acdea6c34b12974deb44e3d2a66675c8c19a8188163'
api_secret = 'fabdda6763a3a539ea316b9fb149e9711c6b04d933a826c28e1fee94351aa178'
client = Client(api_key, api_secret, testnet=True)
buyorder = client.futures_create_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=0.001)
