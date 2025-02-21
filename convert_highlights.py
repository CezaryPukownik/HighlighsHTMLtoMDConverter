#! /usr/bin/python3

import base64
import os
import pathlib
import re
import uuid
from urllib.parse import unquote

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

INPUT_FOLDER = "highlights_html"
OUTPUT_FOLDER = "highlights_md"
IMAGES_FOLDER = "highlights_md/images"

# Ensure images directory exists
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# Parse HTML Highlight
for file in os.listdir(INPUT_FOLDER):
    filepath = pathlib.Path(INPUT_FOLDER, file)

    if not file.endswith(".html"):
        continue

    source_file_name = file.rsplit(".", 1)[0]

    print(f"Converting: {filepath}", end=": ")
    try:
        with open(filepath, "r") as f:
            soup = BeautifulSoup(f.read(), "lxml")

            heading = soup.find("h1").text
            pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (.*)"
            created_at, book_title = re.match(pattern, heading).group(1, 2)

            book_author = soup.find("span").text

            notes = soup.body.find_all("div", recursive=False, id=True)

            parsed_notes = []
            img_counter = 0

            for note_tag in notes:
                note_data = {}

                if page := note_tag.find(class_="bm-page"):
                    note_data["page"] = page.text.strip()

                if note := note_tag.find(class_="bm-note"):
                    note_data["note"] = note.text.strip()

                if text := note_tag.find(class_="bm-text"):
                    note_data["text"] = text.text.strip()

                # Handle images
                if img_div := note_tag.find(class_="bm-image"):
                    if img_tag := img_div.find("img"):
                        img_counter += 1
                        img_filename = f"{source_file_name}_img_{img_counter:05d}.png"
                        img_path = os.path.join(IMAGES_FOLDER, img_filename)

                        # Extract and save the image
                        if img_tag.get("src") and img_tag["src"].startswith(
                            "data:image"
                        ):
                            # For base64 encoded images
                            img_data = img_tag["src"].split(",", 1)[1]
                            try:
                                with open(img_path, "wb") as img_file:
                                    img_file.write(base64.b64decode(img_data))
                                note_data["image"] = img_path
                            except Exception as e:
                                print(f"Error saving image: {e}")
                        elif img_tag.get("src"):
                            # For URL-based images (you might need additional handling for external URLs)
                            src_path = unquote(img_tag["src"])
                            if os.path.isfile(src_path):
                                # Copy the image to the images folder
                                with open(src_path, "rb") as src_img, open(
                                    img_path, "wb"
                                ) as dest_img:
                                    dest_img.write(src_img.read())
                                note_data["image"] = img_path
                            else:
                                print(f"Warning: Image not found at {src_path}")

                parsed_notes.append(note_data)

        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("highlights_template.md.j2")
        highlights_md = template.render(
            title=book_title,
            author=book_author,
            created_at=created_at,
            notes=parsed_notes,
        )

        filepath = pathlib.Path(OUTPUT_FOLDER, file).with_suffix(".md")
        with open(filepath, "w") as f:
            f.write(highlights_md)
        print("SUCCESS!")
    except Exception as e:
        print(f"FAILED! Error: {e}")
