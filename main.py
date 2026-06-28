from trade_reader import read_trade_db
from fifo import group_by_ticker
from fifo import process_fifo

trades = read_trade_db()

trades.sort(key=lambda x: x["date"])

groups = group_by_ticker(trades)

results = process_fifo(groups)

for ticker, result in results.items():

    print(f"\n===== {ticker} =====")

    print("총 실현수익:", result["profit"])

    print("잔량")

    for page_id, qty in result["remaining"].items():
        print(page_id, qty)
