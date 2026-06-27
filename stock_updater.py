from notion_client import Client
import yfinance as yf
import os

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
    ticker_data = props["티커"]["rich_text"]

    if len(ticker_data) == 0:
        print("티커가 비어있어 건너뜀")
        continue

    ticker = ticker_data[0]["plain_text"]

    try:
        stock = yf.Ticker(ticker)

        # 현재가 가져오기
        hist = stock.history(period="1d")

        if hist.empty:
            print(f"{ticker}: 주가 정보를 찾을 수 없음")
            continue

        current_price = float(hist["Close"].iloc[-1])

        # 현재가 업데이트
        notion.pages.update(
            page_id=page["id"],
            properties={
                "현재가": {
                    "number": current_price
                }
            }
        )

        print(f"✅ {ticker} → {current_price}")

    except Exception as e:
        print(f"❌ {ticker} 오류: {e}")
