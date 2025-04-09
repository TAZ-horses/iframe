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

        # Pull each property safely (falling back if not found)
        category_prop  = props.get("Category", {})
        service_prop   = props.get("Service", {})
        username_prop  = props.get("Username", {})
        password_prop  = props.get("Password", {})
        desc_prop      = props.get("Description", {})
        notes_prop     = props.get("Notes", {})

        # --------- Category (flexible fallback) ---------
        # 1) If it's a "select" property, use select["name"]
        # 2) If it's "rich_text", use the first .plain_text
        # 3) If it's "title", use the first .plain_text
        # 4) Otherwise "Uncategorized"
        category = "Uncategorized"
        if "select" in category_prop and category_prop["select"]:
            category = category_prop["select"].get("name", "Uncategorized")
        elif "rich_text" in category_prop and category_prop["rich_text"]:
            category = category_prop["rich_text"][0].get("plain_text", "Uncategorized")
        elif "title" in category_prop and category_prop["title"]:
            category = category_prop["title"][0].get("plain_text", "Uncategorized")

        # --------- Service (usually a 'title' property) ---------
        service = "Unknown"
        if "title" in service_prop and service_prop["title"]:
            service = service_prop["title"][0].get("plain_text", "Unknown")
        elif "rich_text" in service_prop and service_prop["rich_text"]:
            service = service_prop["rich_text"][0].get("plain_text", "Unknown")

        # --------- Username (rich_text fallback) ---------
        username = ""
        if "rich_text" in username_prop and username_prop["rich_text"]:
            username = username_prop["rich_text"][0].get("plain_text", "")

        # --------- Password (rich_text fallback) ---------
        password = ""
        if "rich_text" in password_prop and password_prop["rich_text"]:
            password = password_prop["rich_text"][0].get("plain_text", "")

        # --------- Description & Notes ---------
        description = ""
        if "rich_text" in desc_prop and desc_prop["rich_text"]:
            description = desc_prop["rich_text"][0].get("plain_text", "")

        notes = ""
        if "rich_text" in notes_prop and notes_prop["rich_text"]:
            notes = notes_prop["rich_text"][0].get("plain_text", "")

        # Add to the structured dictionary
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
