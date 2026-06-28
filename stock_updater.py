from notion_client import Client
import yfinance as yf
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# GitHub Secrets
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

# Notion 연결
notion = Client(auth=NOTION_TOKEN)

# 데이터베이스 조회
response = notion.databases.query(database_id=DATABASE_ID)

for page in response["results"]:

    props = page["properties"]

    # 티커 읽기 (Text 속성)
    ticker_data = props["현재가 DB_티커"]["rich_text"]

    if len(ticker_data) == 0:
        print("티커가 비어있어 건너뜀")
        continue

    ticker = ticker_data[0]["plain_text"]

    try:
        stock = yf.Ticker(ticker)

        info = stock.info
        market_cap = info.get("marketCap")

        # 최근 2거래일 데이터 조회
        hist = stock.history(period="5d")

        if len(hist) < 2:
            print(f"{ticker}: 데이터 부족")
            continue

        current_price = float(hist["Close"].iloc[-1])
        previous_price = float(hist["Close"].iloc[-2])

        change = current_price - previous_price

        
        update_time = datetime.now(
            ZoneInfo("Asia/Seoul")
        ).strftime("%Y-%m-%d %H:%M")

        # 현재가 업데이트
        notion.pages.update(
            page_id=page["id"],
            properties={
                "현재가": {
                    "number": current_price
                },
                "전일대비": {
                    "number": change
                },
                "시가총액": {
                    "number": market_cap
                },
                "마지막 업데이트": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": update_time
                            }
                        }
                    ]
                }
            }
        )

        print(f"✅ {ticker} → {current_price}")

    except Exception as e:
        print(f"❌ {ticker} 오류: {e}")
