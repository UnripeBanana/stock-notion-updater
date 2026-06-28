from trade_reader import read_trade_db
from fifo import group_by_ticker

trades = read_trade_db()

trades.sort(key=lambda x: x["date"])

groups = group_by_ticker(trades)

for ticker, items in groups.items():

    print(f"\n===== {ticker} =====")

    for t in items:
        print(t)
