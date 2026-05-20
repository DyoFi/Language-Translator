from flask import Flask, render_template, request
import pytesseract
from PIL import Image
from deep_translator import GoogleTranslator
from langdetect import detect
from nltk.corpus import wordnet
import nltk
nltk.download("wordnet")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home_page():
    synonyms = []

    translated_text = ""
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        target_language = request.form.get("language", "en")

        if text:
            try:
                translated_text = GoogleTranslator(source = "auto", target = target_language).translate(text)
                detected_language = detect(text)
                if detected_language != "en":
                    text_english = GoogleTranslator(source = "auto", target = "en").translate(text)
                else:
                    text_english = text

                for syn in wordnet.synsets(text_english, lang = "eng"):
                    for lemma in syn.lemmas():
                        if lemma.name() not in synonyms:
                            synonyms.append(lemma.name())

                if not synonyms:
                    synonyms.append("No synonyms found in English")

                
            except Exception as e:
                translate = "Error"
                synonyms = ["Error fetching synonyms"]

    return render_template(
        "index.html",
        text = text,
        translated_text = translated_text,
        synonyms = synonyms
    )

if __name__ == "__main__":
    app.run(debug = True)