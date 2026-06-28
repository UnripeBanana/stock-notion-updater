from notion_client import Client
import os

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
TRADE_DB_ID = os.environ["NOTION_TRADE_DB_ID"]

notion = Client(auth=NOTION_TOKEN)


def read_trade_db():
    response = notion.databases.query(
        database_id=TRADE_DB_ID
    )

    return response["results"]
