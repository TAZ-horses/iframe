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
        service_prop  = props.get("Service", {})
        username_prop = props.get("Username", {})
        password_prop = props.get("Password", {})
        desc_prop     = props.get("Description", {})
        notes_prop    = props.get("Notes", {})

        # ---------- Category (Safe Fallback) -----------
        category = "Uncategorized"
        if "select" in category_prop and category_prop["select"]:
            category = category_prop["select"].get("name", "Uncategorized")
        elif "rich_text" in category_prop and len(category_prop["rich_text"]) > 0:
            category = category_prop["rich_text"][0].get("plain_text", "Uncategorized")
        elif "title" in category_prop and len(category_prop["title"]) > 0:
            category = category_prop["title"][0].get("plain_text", "Uncategorized")

        # ---------- Service (Safe Fallback) -----------
        service = "Unknown"
        if "title" in service_prop and len(service_prop["title"]) > 0:
            service = service_prop["title"][0].get("plain_text", "Unknown")
        elif "rich_text" in service_prop and len(service_prop["rich_text"]) > 0:
            service = service_prop["rich_text"][0].get("plain_text", "Unknown")

        # ---------- Username (Safe Fallback) -----------
        username = ""
        if "rich_text" in username_prop and len(username_prop["rich_text"]) > 0:
            username = username_prop["rich_text"][0].get("plain_text", "")

        # ---------- Password (Safe Fallback) -----------
        password = ""
        if "rich_text" in password_prop and len(password_prop["rich_text"]) > 0:
            password = password_prop["rich_text"][0].get("plain_text", "")

        # ---------- Description (Safe Fallback) ----------
        description = ""
        if "rich_text" in desc_prop and len(desc_prop["rich_text"]) > 0:
            description = desc_prop["rich_text"][0].get("plain_text", "")

        # ---------- Notes (Safe Fallback) ----------
        notes = ""
        if "rich_text" in notes_prop and len(notes_prop["rich_text"]) > 0:
            notes = notes_prop["rich_text"][0].get("plain_text", "")

        # ---------- Build the structured dict ----------
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
