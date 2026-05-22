from flask import Flask, render_template, request
import pickle
import pdfplumber
from docx import Document
import os

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Extract text from PDF
def extract_pdf_text(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text


# Extract text from DOCX
def extract_docx_text(file_path):

    text = ""

    doc = Document(file_path)

    for para in doc.paragraphs:

        text += para.text + " "

    return text


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "resume" not in request.files:

        return render_template(
            "index.html",
            prediction_text="No file uploaded"
        )

    file = request.files["resume"]

    if file.filename == "":

        return render_template(
            "index.html",
            prediction_text="No file selected"
        )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(file_path)

    text = ""

    # PDF
    if file.filename.endswith(".pdf"):

        text = extract_pdf_text(file_path)

    # DOCX
    elif file.filename.endswith(".docx"):

        text = extract_docx_text(file_path)

    else:

        return render_template(
            "index.html",
            prediction_text="Only PDF and DOCX files allowed"
        )

    # Transform and predict
    resume_vector = tfidf.transform([text])

    prediction = model.predict(resume_vector)[0]

    return render_template(
        "index.html",
        prediction_text=f"Predicted Category: {prediction}"
    )


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)