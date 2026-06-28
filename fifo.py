from collections import defaultdict

def group_by_ticker(trades):

    grouped = defaultdict(list)

    for trade in trades:
        grouped[trade["ticker"]].append(trade)

    return grouped
