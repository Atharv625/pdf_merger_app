from flask import Flask, request, render_template, send_file
from pypdf import PdfReader, PdfWriter
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf_files = request.files.getlist("pdfs")
        writer = PdfWriter()

        for file in pdf_files:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            reader = PdfReader(filepath)
            for page in reader.pages:
                writer.add_page(page)

        output_path = os.path.join(UPLOAD_FOLDER, "Merged_BY_ALPHA.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")  # Will look inside templates/

if __name__ == "__main__":
    app.run(debug=True)
