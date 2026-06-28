from collections import defaultdict, deque


def group_by_ticker(trades):
    grouped = defaultdict(list)

    for trade in trades:
        grouped[trade["ticker"]].append(trade)

    return grouped

def process_fifo(grouped_trades):

    results = {}

    for ticker, trades in grouped_trades.items():

        queue = deque()
        realized_profit = 0

        for trade in trades:

            # 매수
            if trade["type"] == "매수":

                queue.append({
                    "page_id": trade["page_id"],
                    "qty": trade["qty"],
                    "price": trade["price"]
                })

            # 매도
            else:

                sell_qty = trade["qty"]

                while sell_qty > 0:

                    oldest = queue[0]

                    matched = min(
                        sell_qty,
                        oldest["qty"]
                    )

                    realized_profit += (
                        trade["price"] - oldest["price"]
                    ) * matched

                    oldest["qty"] -= matched
                    sell_qty -= matched

                    if oldest["qty"] == 0:
                        queue.popleft()

        results[ticker] = {
            "queue": list(queue),
            "profit": realized_profit
        }

    return results
