from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
from model import predict_image, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': f'File type .{ext} not allowed'}), 400
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    result = predict_image(path)
    return jsonify(result)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def _is_image_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        return False
    ext = os.path.splitext(parsed.path)[1].lower().lstrip('.')
    return ext in ALLOWED_EXTENSIONS


def download_image(url):
    """Download an image from a URL. If the URL looks like a page, try to extract
    an image (og:image or first <img>). Returns local path or raises Exception."""
    session = requests.Session()
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    content_type = resp.headers.get('content-type', '')

    # If response is an image, save it directly
    if 'image' in content_type or _is_image_url(url):
        ext = os.path.splitext(urlparse(url).path)[1] or '.jpg'
        filename = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(path, 'wb') as f:
            f.write(resp.content)
        return path

    # Otherwise try to parse HTML and find the main image
    soup = BeautifulSoup(resp.text, 'html.parser')
    # prefer og:image
    og = soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'og:image'})
    img_url = None
    if og and og.get('content'):
        img_url = urljoin(url, og['content'])
    else:
        img = soup.find('img')
        if img and img.get('src'):
            img_url = urljoin(url, img['src'])

    if not img_url:
        raise ValueError('No image found at provided URL')

    # download the discovered image
    img_resp = session.get(img_url, timeout=10)
    img_resp.raise_for_status()
    parsed = urlparse(img_url)
    ext = os.path.splitext(parsed.path)[1] or '.jpg'
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(path, 'wb') as f:
        f.write(img_resp.content)
    return path


@app.route('/predict_url', methods=['POST'])
def predict_url():
    """Accepts JSON {"url": "http://..."} and returns the same predict_image output."""
    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({'error': 'No url provided'}), 400
    url = data['url']
    try:
        path = download_image(url)
    except Exception as e:
        return jsonify({'error': f'Could not fetch image: {str(e)}'}), 400
    try:
        result = predict_image(path)
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
    # include the served uploads URL so clients can preview
    result['image_url'] = url_for('uploaded_file', filename=os.path.basename(path), _external=True)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
