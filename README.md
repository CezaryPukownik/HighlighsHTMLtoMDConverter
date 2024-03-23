# PocketBook Highlights Converter

This project aims to convert PocketBook's HTML exported Highlights into Markdown format. 

I enjoy reading books and then transferring my Highlights to Notion. However, the format of 
exported PocketBook highlights made this process quite challenging. Hence, I developed 
this simple script to simplify the task.

## Usage

1. Create a `.venv` environment and install the dependencies listed in `requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy all `*.html` notes from PocketBook into the `highlights_html` folder.
3. Execute the `convert_highlights.py` script.

```bash
python convert_highlights.py
```

All files will be converted to `*.md` format and saved in the `highlights_md` folder.