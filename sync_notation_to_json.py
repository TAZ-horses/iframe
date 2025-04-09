import os, requests, json

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DB_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
res = requests.post(url, headers=headers)

data = res.json()
mindmap = {}

for result in data.get("results", []):
    props = result["properties"]
    category = props.get("Category", {}).get("select", {}).get("name", "Uncategorized")
    service = props.get("Service", {}).get("title", [{}])[0].get("text", {}).get("content", "")
    username = props.get("Username", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
    password = props.get("Password", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
    if not service:
        continue
    mindmap.setdefault(category, []).append({
        "service": service, "username": username, "password": password
    })

with open("mindmap_data.json", "w") as f:
    json.dump(mindmap, f, indent=2)
