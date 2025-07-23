import os
from typing import List, Dict, Any
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util

# Load model once
MODEL = SentenceTransformer('all-MiniLM-L6-v2')


def extract_outline_from_pdf(pdf_path: str) -> Dict[str, Any]:
    reader = PdfReader(pdf_path)
    all_text_items = []
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        lines = text.split('\n')
        for line in lines:
            if line.strip():
                all_text_items.append({
                    'text': line.strip(),
                    'page': page_num + 1
                })
    # Title: largest/first non-empty line on first page
    title = all_text_items[0]['text'] if all_text_items else 'Untitled Document'
    # Heuristic: semantic ranking for headings
    query = "section heading or title"
    query_emb = MODEL.encode(query)
    for item in all_text_items:
        item['score'] = float(util.cos_sim(MODEL.encode(item['text'][:512]), query_emb)[0])
    # Top N headings by score, assign levels by score
    sorted_items = sorted(all_text_items, key=lambda x: x['score'], reverse=True)
    outline = []
    for idx, item in enumerate(sorted_items[:20]):
        if item['score'] < 0.2:
            continue
        level = 'H1' if idx < 3 else ('H2' if idx < 10 else 'H3')
        outline.append({
            'level': level,
            'text': item['text'],
            'page': item['page']
        })
    return {
        'title': title,
        'outline': outline
    }


def extract_outlines_from_pdfs(pdf_paths: List[str]) -> List[Dict[str, Any]]:
    return [extract_outline_from_pdf(path) for path in pdf_paths] 