#turn input files into plain text, one entry per page of pdf or slide
#entries are formatted like: {"location": "page 3", "text": "..."}

from pathlib import Path

import pymupdf
from pptx import Presentation


def extract_pages(file_path):
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        pages = extract_pdf(path)
    elif extension == ".pptx":
        pages = extract_pptx(path)
    else:
        raise ValueError(f"unsupported file type: {extension} (only .pdf or .pptx)")

    #drop files without text
    pages_with_text = []
    for page in pages:
        if page["text"].strip() != "":
            pages_with_text.append(page)

    return pages_with_text


def extract_pdf(path):
    pages = []
    document = pymupdf.open(path)

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()
        pages.append({"location": f"page {page_number}", "text": text.strip()})

    document.close()
    return pages


def extract_pptx(path):
    pages = []
    presentation = Presentation(path)

    for slide_number, slide in enumerate(presentation.slides, start=1):
        lines = []

        #get text on slide
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    line = "".join(run.text for run in paragraph.runs).strip()
                    if line != "":
                        lines.append(line)

        #get speaker notes
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
            if notes != "":
                lines.append("Speaker notes: " + notes)

        pages.append({"location": f"slide {slide_number}", "text": "\n".join(lines)})

    return pages


def pages_to_text(pages):
    #join pages into a string
    parts = []
    for page in pages:
        #keep track of the locations for later citing
        parts.append(f"[{page['location']}]\n{page['text']}")
    return "\n\n".join(parts)
