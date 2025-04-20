import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from backend.blip_caption import generate_caption
from backend.groq_client import get_medical_report
from backend.pdf_generator import generate_pdf_report

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
PDF_FOLDER = 'static/pdf'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------- ROUTES ---------------- #

# 🏥 Health check route
@app.route('/health')
def health_check():
    return "✅ Server is running"

# 🏠 Home Page
@app.route('/')
def index():
    return render_template('index.html')

# 📤 Upload Page (GET)
@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

# 📄 Upload Form Submission (POST)
@app.route('/upload', methods=['POST'])
def handle_upload():
    try:
        print("🟢 Received upload request")
        image = request.files['image']
        if not image:
            print("🔴 No image file received")
            return render_template('error.html', error="No file uploaded.")

        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
        print(f"✅ Saved image to: {image_path}")

        # Generate caption
        print("🧠 Generating caption...")
        caption = generate_caption(image_path)
        print(f"🧾 Caption: {caption}")

        # Get AI-generated diagnosis
        print("📡 Calling Groq API...")
        report = get_medical_report(caption)
        print("✅ Report generated.")

        # Save report as PDF
        pdf_filename = f"medical_report_{os.path.splitext(filename)[0]}.pdf"
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        generate_pdf_report(report, pdf_path)
        print(f"📄 PDF saved at: {pdf_path}")

        return render_template('success.html', pdf_file=pdf_filename)

    except Exception as e:
        print(f"❌ Exception: {e}")
        return render_template("error.html", error=str(e))

# 📥 PDF Download
@app.route('/download/<filename>')
def download_pdf(filename):
    path = os.path.join(PDF_FOLDER, filename)
    return send_file(path, as_attachment=True)

# ❌ 404 Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", error="Page not found"), 404

# Run locally
if __name__ == "__main__":
    app.run(debug=True)

@app.route('/health')
def health():
    return "✅ Flask app is running"

