# test_notion.py
import os
from dotenv import load_dotenv
from notion_client import Client

# Load environment variables
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

# Try fetching the database info
try:
    response = notion.databases.retrieve(NOTION_DATABASE_ID)
    print("Notion token works! Database name:", response["title"][0]["text"]["content"])
except Exception as e:
    print("Failed to access Notion database:", e)