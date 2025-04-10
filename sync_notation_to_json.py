from notion_client import Client
import os
import json
from dotenv import load_dotenv
import logging

# Logging config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ICON_MAP = {
    "Hosting": "🖥️",
    "Development": "🛠️",
    "Social Media": "📱",
    "Business Tools": "📂",
    "Design": "🎨",
    "Admin": "🗂️",
    "Marketing": "📈",
    "Default": "🧩"
}

def get_property_value(prop, prop_type='text'):
    try:
        if prop_type == 'text':
            return prop['rich_text'][0]['plain_text'] if prop.get('rich_text') else ''
        elif prop_type == 'title':
            return prop['title'][0]['plain_text'] if prop.get('title') else ''
        elif prop_type == 'select':
            return prop['select']['name'] if prop.get('select') else 'Uncategorized'
        return ''
    except (KeyError, IndexError, TypeError) as e:
        logger.warning(f"Property parse error: {e}")
        return ''

def fetch_notion_database(database_id, notion):
    results, next_cursor = [], None
    while True:
        query = {"database_id": database_id}
        if next_cursor:
            query["start_cursor"] = next_cursor
        response = notion.databases.query(**query)
        results.extend(response.get("results", []))
        if not response.get("has_more"): break
        next_cursor = response.get("next_cursor")
    logger.info(f"✅ Fetched {len(results)} entries")
    return results

def parse_notion_data(pages):
    structured = {}
    for page in pages:
        try:
            props = page.get("properties", {})
            service = get_property_value(props.get("Service", {}), "title")
            if not service:
                continue

            category = get_property_value(props.get("Category", {}), "select")
            icon = ICON_MAP.get(category, ICON_MAP["Default"])

            entry = {
                "title": service,
                "description": get_property_value(props.get("Description", {}), "text"),
                "username": get_property_value(props.get("Username", {}), "text"),
                "notes": get_property_value(props.get("Notes", {}), "text"),
                "password": get_property_value(props.get("Password", {}), "text"),
                "icon": icon
            }
            structured.setdefault(category, []).append(entry)
        except Exception as e:
            logger.error(f"Parse error on page {page.get('id')}: {e}")
            continue
    return structured

def main():
    load_dotenv()
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not notion or not database_id:
        logger.error("Missing environment variables.")
        raise SystemExit(1)

    pages = fetch_notion_database(database_id, notion)
    data = parse_notion_data(pages)

    with open("mindmap_data_synced.json", "w") as f:
        json.dump(data, f, indent=2)
        logger.info("✅ mindmap_data_synced.json written successfully")

if __name__ == "__main__":
    main()
