import os
from dotenv import load_dotenv
import gspread
from notion_client import Client
from datetime import datetime


#Load Notion Credential
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

#Set up google sheets
gc = gspread.service_account(filename='credentials.json')

#get data from sheets
sheet_name = 'DeepNeuron'
sheet = gc.open(sheet_name).sheet1
rows  = sheet.get_all_records()

#Setup the notion
notion = Client(auth=NOTION_TOKEN)

def add_to_notion(row):
    #get specific elements from rows
    task_title = row["Task Title"]
    source_branch = row["Source Branch"]
    description = row["Description of Tasks"]
    task_type = row["Type of Task"]
    general_enquiries = row["General Enquires"]
    due_date = row["Due Date"]
    due_date_obj = datetime.strptime(due_date, "%m/%d/%Y")
    due_date_iso = due_date_obj.strftime("%Y-%m-%d")

    properties = {
    "Task Title": {"title": [{"text": {"content": task_title}}]},
    "Source Branch": {"select": {"name": source_branch}},
    "Description": {"rich_text": [{"text": {"content": description}}]},
    "Type of Task": {"select": {"name": task_type}},
    "General Enquiries": {"rich_text": [{"text": {"content": general_enquiries}}]},
    "Due Date": {"date": {"start": due_date_iso}},
    "Status": {"status": {"name": "Not started"}},
    "Assigned To": {"people": [] } # Empty placeholder
    }

    # Create page
    notion.pages.create(
    parent={"database_id": NOTION_DATABASE_ID},
    properties=properties
    )

    print(f"Added ticket: {source_branch} - {task_title}")

#Process each form

for i, row in enumerate(rows, start=2):  
    try:
        if row.get("Processed", "").lower() == "yes":
            #print(f"Skipping already processed row {i}")
            continue

        add_to_notion(row)

        sheet.update_cell(i, sheet.find("Processed").col, "Yes")

    except Exception as e:
        print(f"Failed to process row {i}: {row}, error: {e}")



