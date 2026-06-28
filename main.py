from trade_reader import read_trade_db
from fifo import group_by_ticker
from fifo import process_fifo

trades = read_trade_db()

trades.sort(key=lambda x: x["date"])

groups = group_by_ticker(trades)

results = process_fifo(groups)

for ticker, result in results.items():

    print(f"\n===== {ticker} =====")

    print("잔량")

    for page_id, qty in result["remaining"].items():
        print(page_id, qty)

    print("매도별 실현수익")

    for page_id, profit in result["profit_by_sell"].items():
        print(page_id, profit)

    print("누적 실현수익:", result["profit"])
