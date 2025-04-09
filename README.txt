# Steed Media Mindmap Deployment

## GitHub Action Setup
1. Go to your GitHub repo `iframe` → Settings → Secrets → Actions.
2. Add two secrets:
   - `NOTION_TOKEN`: Your Notion integration token
   - `NOTION_DB_ID`: Your Notion database ID (like `1d0cc957949480e180dcfeb4cd5eea19`)
3. Push the following files:
   - `sync_notation_to_json.py`
   - `.github/workflows/notion-sync.yml`
   - `login.html`

## Embedding in Square Online
Use this code in your Square Online embed block:

<iframe src="https://taz-horses.github.io/iframe/login.html" width="100%" height="800" style="border:none;"></iframe>

## Password
Default password: `steed2025`
To change it, edit the `login.html` file.
