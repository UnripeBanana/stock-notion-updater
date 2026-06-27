from notion_client import Client
import yfinance as yf
import os

# GitHub Secrets에서 가져오기
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

notion = Client(auth=NOTION_TOKEN)

# 데이터베이스 조회
response = notion.databases.query(database_id=DATABASE_ID)

for page in response["results"]:

    properties = page["properties"]

    # 티커 읽기
    ticker = properties["티커"]["rich_text"]

    if len(ticker) == 0:
        continue

    ticker = ticker[0]["plain_text"]

    try:
        # Yahoo Finance에서 현재가 가져오기
        stock = yf.Ticker(ticker)
        price = stock.fast_info["lastPrice"]

        # 노션 업데이트
        notion.pages.update(
            page_id=page["id"],
            properties={
                "현재가": {
                    "number": float(price)
                }
            }
        )

        print(f"{ticker} → {price}")

    except Exception as e:
        print(f"{ticker} 실패:", e)
