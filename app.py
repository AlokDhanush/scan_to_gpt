from flask import Flask, render_template, request, redirect, url_for, jsonify
import pytesseract
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os
import subprocess
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pytesseract.pytesseract.tesseract_cmd = "E:/Tesseract-data/tesseract.exe"  # Change as needed

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file uploaded", 400

        file = request.files['image']
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        # OCR
        img = cv2.imread(path)
        text = pytesseract.image_to_string(img)

        # Save for pasting
        with open("last_extracted.txt", "w", encoding="utf-8") as f:
            f.write(text)

        return render_template('index.html', text=text)

    return render_template('index.html', text=None)

@app.route('/paste', methods=['POST'])
def paste_to_chatgpt():
    try:
        subprocess.Popen(["python", "auto_paste.py"])
        return redirect(url_for('index'))
    except Exception as e:
        return f"Failed to run auto_paste.py: {e}"

@app.route('/capture', methods=['POST'])
def capture_image():
    try:
        data = request.get_json(silent=True)
        if not data or 'imageData' not in data:
            return jsonify({"error": "No image data provided"}), 400

        data_url: str = data['imageData']
        if ',' not in data_url:
            return jsonify({"error": "Invalid data URL"}), 400

        header, encoded = data_url.split(',', 1)
        try:
            image_bytes = base64.b64decode(encoded)
        except Exception:
            return jsonify({"error": "Failed to decode image"}), 400

        np_buffer = np.frombuffer(image_bytes, dtype=np.uint8)
        image_bgr = cv2.imdecode(np_buffer, cv2.IMREAD_COLOR)
        if image_bgr is None:
            return jsonify({"error": "Failed to read image"}), 400

        text = pytesseract.image_to_string(image_bgr)

        with open("last_extracted.txt", "w", encoding="utf-8") as f:
            f.write(text)

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)