from notion_client import Client
import os
import json
from dotenv import load_dotenv

load_dotenv()
notion_token = os.getenv("NOTION_TOKEN")
database_id = "1d0cc957949480e180dcfeb4cd5eea19"

notion = Client(auth=notion_token)

def fetch_notion_database(database_id):
    results = []
    next_cursor = None
    while True:
        response = notion.databases.query(
            **({
                "database_id": database_id,
                "start_cursor": next_cursor
            } if next_cursor else {
                "database_id": database_id
            })
        )
        results.extend(response["results"])
        if not response.get("has_more"):
            break
        next_cursor = response["next_cursor"]
    return results

def parse_notion_data(pages):
    structured = {}
    for page in pages:
        props = page["properties"]
        category_prop = props.get("Category", {})
        service_prop = props.get("Service", {})
        username_prop = props.get("Username", {})
        password_prop = props.get("Password", {})
        notes_prop = props.get("Notes", {})

        category_prop = props["Category"]
category = "Uncategorized"

if "select" in category_prop and category_prop["select"]:
    category = category_prop["select"]["name"]
elif "rich_text" in category_prop and category_prop["rich_text"]:
    category = category_prop["rich_text"][0]["plain_text"]
elif "title" in category_prop and category_prop["title"]:
    category = category_prop["title"][0]["plain_text"]
        )
        service = (
            service_prop.get("title", [{}])[0].get("plain_text") or
            "Unknown"
        )
        username = username_prop.get("rich_text", [{}])[0].get("plain_text", "")
        password = password_prop.get("rich_text", [{}])[0].get("plain_text", "")
        description = notes_prop.get("rich_text", [{}])[0].get("plain_text", "")

        structured.setdefault(category, []).append({
            "service": service,
            "username": username,
            "password": password,
            "description": description
        })
    return structured

pages = fetch_notion_database(database_id)
structured_data = parse_notion_data(pages)

with open("mindmap_data_synced.json", "w") as f:
    json.dump(structured_data, f, indent=2)
