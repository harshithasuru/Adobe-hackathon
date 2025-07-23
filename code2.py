import os
import sys
import json
from datetime import datetime
from backend.extractor import extract_outline_from_pdf

def extract_subsection(text):
    # Heuristic: up to 3 sentences, max 350 chars
    sentences = text.replace('\n', ' ').split('. ')
    out = '. '.join(sentences[:3])[:350]
    return out

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Process combined input JSON and output final JSON (Challenge 1B schema)')
    parser.add_argument('--input', required=True, help='Input combined JSON file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Expecting input as dict with metadata and documents
    metadata = data.get('metadata') or data.get('METADATA') or {}
    documents = data.get('documents') or data.get('DOCUMENTS') or []
    if not documents and 'input_documents' in metadata:
        # Fallback: try to build document list from input_documents
        documents = [{'filename': fn} for fn in metadata['input_documents']]

    extracted_sections = []
    subsection_analysis = []

    for doc in documents:
        pdf_name = doc.get('filename') or doc.get('document')
        pdf_path = doc.get('pdf_path') or pdf_name
        if not pdf_path or not os.path.exists(pdf_path):
            continue
        outline = extract_outline_from_pdf(pdf_path)
        # Top 2 sections by importance (score)
        for idx, section in enumerate(outline['outline'][:2]):
            extracted_sections.append({
                'document': pdf_name,
                'section_title': section['text'],
                'importance_rank': idx + 1,
                'page_number': section['page']
            })
            subsection_analysis.append({
                'document': pdf_name,
                'refined_text': extract_subsection(section['text']),
                'page_number': section['page']
            })

    output = {
        'metadata': {
            **metadata,
            'processing_timestamp': datetime.now().isoformat()
        },
        'extracted_sections': extracted_sections,
        'subsection_analysis': subsection_analysis
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    print(f'Wrote {args.output}')

if __name__ == '__main__':
    main()