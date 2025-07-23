# PDF Outline Extraction Hackathon Project

## Setup

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. (Optional) Download sentence-transformers model in advance for offline use.

## Running the Backend API

```bash
cd backend
python app.py
```
- The API will be available at http://localhost:5000/extract-outline
- Use a tool like Postman or the web interface to upload PDF(s) and get JSON output.

## Running the CLI Scripts

### Challenge 1A (Single PDF or Directory)
```bash
python code1.py --input Challenge_1a/sample_dataset/pdfs --output Challenge_1a/sample_dataset/outputs
```
- Outputs individual JSONs for each PDF in the output directory.

### Challenge 1B (Batch Processing)
```bash
python code2.py --input Challenge_1b/Collection\ 1/challenge1b_input.json --output Challenge_1b/Collection\ 1/challenge1b_output.json
```
- Reads combined input JSON, outputs final JSON.

## Web Interface

- Open `index.html` in your browser.
- For backend-powered extraction, update the JS to POST PDFs to `/extract-outline` and display the returned JSON.

## Notes
- All outputs match the schema in `Challenge_1a/sample_dataset/schema/output_schema.json`.
- Backend and scripts use the same extraction logic for consistency.