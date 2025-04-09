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
        # Process Category using a default get() method: assume it is a select type.
        # If it's not, the default "Uncategorized" will be used.
        category = props["Category"].get("select", {}).get("name", "Uncategorized")
        service = props["Service"]["title"][0]["plain_text"] if props["Service"]["title"] else "Unknown"
        username = props["Username"]["rich_text"][0]["plain_text"] if props["Username"]["rich_text"] else ""
        password = props["Password"]["rich_text"][0]["plain_text"] if props["Password"]["rich_text"] else ""
        description = props["Description"]["rich_text"][0]["plain_text"] if props["Description"]["rich_text"] else ""
        notes = props["Notes"]["rich_text"][0]["plain_text"] if props["Notes"]["rich_text"] else ""

        structured.setdefault(category, []).append({
            "service": service,
            "username": username,
            "password": password,
            "description": description,
            "notes": notes
        })
    return structured

pages = fetch_notion_database(database_id)
structured_data = parse_notion_data(pages)

with open("mindmap_data_synced.json", "w") as f:
    json.dump(structured_data, f, indent=2)
