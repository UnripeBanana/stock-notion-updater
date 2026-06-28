from trade_reader import read_trade_db

trades = read_trade_db()

for trade in trades:
    print(trade)
