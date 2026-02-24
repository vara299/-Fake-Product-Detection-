# Fake Product Detection (Netflix-style UI)

This is a simple **fake product detection** demo application with a Netflix-inspired web UI.
It includes a Flask backend (Python) and a frontend (HTML/CSS/JS) served by Flask.

## Features
- Netflix-like homepage with product cards.
- Upload an image of a product to classify as **Genuine** or **Fake**.
- Lightweight image-based heuristic model (no heavy ML dependencies).
- Runs with Python 3.8+ and Flask.

## Run locally (VS Code)
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in your browser.

## Project structure
```
fake_product_detector/
├─ app.py
├─ model.py
├─ requirements.txt
├─ templates/
│  └─ index.html
├─ static/
│  ├─ css/style.css
│  └─ js/app.js
└─ sample_images/
   ├─ genuine_sample.jpg
   └─ fake_sample.jpg
```

## Notes
- This is a demo with a simple heuristic classifier (image brightness + filename heuristic).
- Replace `model.py` with your trained ML model for real use.
