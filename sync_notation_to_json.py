from notion_client import Client
import os
import json
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_property_value(prop, prop_type='text'):
    """Safely extract property values from Notion API response."""
    try:
        if prop_type == 'text':
            return prop['rich_text'][0]['plain_text'] if prop.get('rich_text') else ''
        elif prop_type == 'title':
            return prop['title'][0]['plain_text'] if prop.get('title') else ''
        elif prop_type == 'select':
            return prop['select']['name'] if prop.get('select') else 'Uncategorized'
        return ''
    except (KeyError, IndexError, TypeError) as e:
        logger.warning(f"Error parsing property: {str(e)}")
        return ''

def fetch_notion_database(database_id, notion):
    """Fetch all pages from a Notion database with pagination."""
    results = []
    next_cursor = None
    
    try:
        while True:
            query_params = {"database_id": database_id}
            if next_cursor:
                query_params["start_cursor"] = next_cursor

            response = notion.databases.query(**query_params)
            results.extend(response.get('results', []))
            
            if not response.get('has_more'):
                break
            next_cursor = response.get('next_cursor')
            
        logger.info(f"Fetched {len(results)} pages from Notion")
        return results
    except Exception as e:
        logger.error(f"Failed to fetch database: {str(e)}")
        raise

def parse_notion_data(pages):
    """Transform Notion API response into structured data."""
    structured = {}
    
    for page in pages:
        try:
            props = page.get('properties', {})
            entry = {
                "description": get_property_value(props.get('Description', {}), 'text'),
                "service": get_property_value(props.get('Service', {}), 'title'),
                "username": get_property_value(props.get('Username', {}), 'text'),
                "notes": get_property_value(props.get('Notes', {}), 'text'),
                "password": get_property_value(props.get('Password', {}), 'text')
            }
            category = get_property_value(props.get('Category', {}), 'select')
            structured.setdefault(category, []).append(entry)
        except Exception as e:
            logger.error(f"Error parsing page {page.get('id')}: {str(e)}")
            continue
            
    return structured

def main():
    """Main execution flow."""
    load_dotenv()
    
    try:
        notion = Client(auth=os.getenv("NOTION_TOKEN"))
        database_id = os.getenv("NOTION_DATABASE_ID", "1d0cc957949480e180dcfeb4cd5eea19")
        
        pages = fetch_notion_database(database_id, notion)
        structured_data = parse_notion_data(pages)
        
        with open("mindmap_data_synced.json", "w") as f:
            json.dump(structured_data, f, indent=2)
            logger.info("Successfully wrote data to mindmap_data_synced.json")
            
    except Exception as e:
        logger.error(f"Critical error in main execution: {str(e)}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
