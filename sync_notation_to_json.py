from notion_client import Client
import os
import json
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Optional: assign emoji per category
CATEGORY_ICONS = {
    "Hosting": "🌐",
    "Development": "💻",
    "Social Media": "📱",
    "Business Tools": "🧰",
    "Design": "🎨",
    "Uncategorized": "🧩"
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
    results = []
    next_cursor = None

    while True:
        response = notion.databases.query(
            **({"database_id": database_id, "start_cursor": next_cursor} if next_cursor else {"database_id": database_id})
        )
        results.extend(response.get("results", []))
        if not response.get("has_more"):
            break
        next_cursor = response.get("next_cursor")
    logger.info(f"Fetched {len(results)} rows from Notion")
    return results

def parse_notion_data(pages):
    structured = {}

    for page in pages:
        try:
            props = page.get('properties', {})
            service = get_property_value(props.get("Service", {}), 'title')
            if not service:
                continue  # Skip entry if Service is missing

            category = get_property_value(props.get("Category", {}), 'select') or "Uncategorized"
            icon = CATEGORY_ICONS.get(category, "🧩")

            entry = {
                "service": service,
                "description": get_property_value(props.get("Description", {}), 'text'),
                "username": get_property_value(props.get("Username", {}), 'text'),
                "password": get_property_value(props.get("Password", {}), 'text'),
                "notes": get_property_value(props.get("Notes", {}), 'text'),
                "icon": icon
            }

            structured.setdefault(category, []).append(entry)
        except Exception as e:
            logger.error(f"Error parsing row: {e}")
            continue

    return structured

def main():
    load_dotenv()
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not notion_token or not database_id:
        logger.error("Missing NOTION_TOKEN or NOTION_DATABASE_ID in environment.")
        return

    notion = Client(auth=notion_token)
    pages = fetch_notion_database(database_id, notion)
    mindmap_data = parse_notion_data(pages)

    with open("mindmap_data_synced.json", "w") as f:
        json.dump(mindmap_data, f, indent=2)
        logger.info("✅ mindmap_data_synced.json written successfully")

if __name__ == "__main__":
    main()
