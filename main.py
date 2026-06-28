from trade_reader import read_trade_db

trades = read_trade_db()

trades.sort(key=lambda x: x["date"])

for trade in trades:
    print(trade)
