"""Remove presenter controls from the rendered student deck only."""
from pathlib import Path
import re

base = Path(__file__).resolve().parent.parent
page = base / 'docs/week-02/index.html'
if page.exists():
    html = page.read_text()
    html = re.sub(r'\s*<script src="[^"]*/plugin/notes/notes\.js"></script>', '', html)
    html = re.sub(r'^\s*RevealNotes,\s*$', '', html, flags=re.M)
    # Quarto serializes its tools menu as JSON inside the initialization script.
    html = re.sub(r'<li[^<>]*>[^<>]*<a[^<>]*speakerMode\(event\)[^<>]*>.*?</a></li>(?:\\n)?', '', html)
    assert not re.search(r'<aside\b[^>]*class="notes"', html)
    assert 'RevealNotes' not in html and 'speakerMode(event)' not in html
    page.write_text(html)
    (page.parent / 'student.html').write_text(html)
