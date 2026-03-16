"""
Microsoft Learn Transcript Extractor

This script downloads Microsoft Learn lesson pages, extracts the readable
lesson text, removes UI elements (navigation, reading time, feedback blocks),
and saves clean transcripts to disk.

Features
--------
- Download lesson HTML pages
- Extract structured lesson text
- Remove UI components (reading time, feedback section)
- Save transcripts as .txt files
- Combine multiple transcripts into one module file

Usage
-----
Run the script and paste lesson URLs when prompted:

    python learn_transcript_extractor.py

Press ENTER on an empty line to start processing.
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

HTML_DIR = "downloaded_HTMLs"
TXT_DIR = "clean_transcripts"

STOP_PHRASES = [
    "was this page helpful",
    "need help with this topic",
    "ask learn"
]

# Ensure output directories exist
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)


# ------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------

def sanitize_filename(url: str) -> str:
    """
    Convert a URL into a safe filename.

    Parameters
    ----------
    url : str
        Lesson URL

    Returns
    -------
    str
        Safe filename derived from the URL path
    """
    parsed = urlparse(url)
    name = parsed.path.strip("/").replace("/", "_")

    if not name:
        name = "index"

    return name


def download_html(url: str) -> str:
    """
    Download a webpage and store it locally as an HTML file.

    Parameters
    ----------
    url : str
        Lesson URL

    Returns
    -------
    str
        Path to the saved HTML file
    """

    print(f"Downloading: {url}")

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    response.raise_for_status()
    response.encoding = response.apparent_encoding

    filename = sanitize_filename(url) + ".html"
    path = os.path.join(HTML_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(response.text)

    return path


def get_content_root(soup: BeautifulSoup):
    """
    Locate the main lesson content container.

    Microsoft Learn pages typically structure content as:
        <main>
            <article>
                lesson content
            </article>
        </main>

    Parameters
    ----------
    soup : BeautifulSoup

    Returns
    -------
    Tag
        Root element containing the lesson text
    """

    main = soup.find("main")

    if not main:
        return soup

    article = main.find("article")

    if article:
        return article

    return main


def extract_clean_text(html_path: str) -> str:
    """
    Extract readable lesson text from a downloaded HTML page.

    The function removes:
    - reading time metadata
    - feedback UI blocks
    - duplicated lines

    Parameters
    ----------
    html_path : str
        Path to the HTML file

    Returns
    -------
    str
        Clean transcript text
    """

    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    root = get_content_root(soup)

    content = []

    for tag in root.find_all(["h1", "h2", "h3", "h4", "p", "li"]):

        text = tag.get_text(" ", strip=True)

        if not text:
            continue

        text_lower = text.lower()

        # Stop extraction when feedback UI starts
        if any(p in text_lower for p in STOP_PHRASES) or text_lower == "feedback":
            break

        # Remove reading-time metadata
        if re.match(r"^\d+\s+minute", text_lower):
            continue

        # Format headings
        if tag.name.startswith("h"):
            content.append("\n" + text.upper())
            content.append("-" * len(text))

        # Format bullet points
        elif tag.name == "li":
            content.append(f"- {text}")

        else:
            content.append(text)

    # Remove duplicates while preserving order
    content = list(dict.fromkeys(content))

    return "\n".join(content)


def save_transcript(text: str, html_path: str) -> str:
    """
    Save extracted lesson text to a transcript file.

    Parameters
    ----------
    text : str
        Extracted transcript
    html_path : str
        Source HTML file path

    Returns
    -------
    str
        Path to the saved transcript
    """

    filename = os.path.basename(html_path).replace(".html", ".txt")
    path = os.path.join(TXT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved transcript: {filename}")

    return path


def combine_transcripts(output_name: str = "module_transcript.txt") -> str:
    """
    Combine all transcript files into a single document.

    Parameters
    ----------
    output_name : str
        Name of the combined output file

    Returns
    -------
    str
        Path to the combined transcript file
    """

    combined = []

    for file in sorted(os.listdir(TXT_DIR)):

        if not file.endswith(".txt"):
            continue

        # Avoid reading the combined file itself
        if file == output_name:
            continue

        path = os.path.join(TXT_DIR, file)

        with open(path, encoding="utf-8") as f:
            combined.append(f.read())

    output_path = os.path.join(TXT_DIR, output_name)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(combined))

    print(f"Combined transcript created: {output_name}")

    return output_path


# ------------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------------

def main():
    """
    Main CLI interface.

    Users can paste multiple lesson URLs directly in the terminal.
    Press ENTER on an empty line to start processing.
    """

    print("Paste Microsoft Learn lesson URLs.")
    print("Press ENTER on an empty line to start processing.\n")

    urls = []

    while True:
        url = input("URL: ").strip()

        if not url:
            break

        urls.append(url)

    if not urls:
        print("No URLs provided.")
        return

    # Process each lesson
    for url in urls:

        html_path = download_html(url)

        text = extract_clean_text(html_path)

        save_transcript(text, html_path)

    # Combine transcripts
    combine_transcripts()

    print("\nAll lessons processed successfully.")


if __name__ == "__main__":
    main()
