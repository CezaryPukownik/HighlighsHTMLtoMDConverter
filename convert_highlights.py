import os
import re
import pathlib
from jinja2 import Environment, FileSystemLoader

from bs4 import BeautifulSoup

INPUT_FOLDER = "highlights_html"
OUTPUT_FOLDER = "highlights_md"

# Parse HTML Highlight
for file in os.listdir(INPUT_FOLDER):
    filepath = pathlib.Path(INPUT_FOLDER, file)
    
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f.read(), 'lxml')


        heading = soup.find('h1').text
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (.*)"
        created_at, book_title = re.match(pattern, heading).group(1, 2)

        book_author = soup.find('span').text

        notes = soup.body.find_all('div', recursive=False, id=True)

        parsed_notes = []
        for note_tag in notes:
            if (page := note_tag.find(class_='bm-page')):
                page = page.text.strip()
            
            if (note := note_tag.find(class_='bm-note')):
                note = note.text.strip()

            if (text := note_tag.find(class_='bm-text')):
                text = text.text.strip()

            parsed_notes.append({
                "page": page,
                "note": note,
                "text": text,
            })

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('highlights_template.md.j2')
    highlights_md = template.render(
       title=book_title,
       author=book_author,
       created_at=created_at,
       notes=parsed_notes 
    )

    filepath = pathlib.Path(OUTPUT_FOLDER, file).with_suffix('.md')
    with open(filepath, 'w') as f:
        f.write(highlights_md)
    
