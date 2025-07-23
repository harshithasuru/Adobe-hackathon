from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
from extractor import extract_outline_from_pdf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/extract-outline', methods=['POST'])
def extract_outline():
    if 'pdfs' not in request.files:
        return jsonify({'error': 'No PDF files uploaded.'}), 400
    files = request.files.getlist('pdfs')
    results = []
    for file in files:
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            temp_path = tmp.name
        # Now the file is closed, safe to use
        outline = extract_outline_from_pdf(temp_path)
        outline['filename'] = filename
        results.append(outline)
        os.unlink(temp_path)
    if len(results) == 1:
        return jsonify(results[0])
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True) 