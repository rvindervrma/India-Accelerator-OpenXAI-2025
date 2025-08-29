import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv


from pdf_utils import extract_text_from_pdf
from quiz_generator import generate_mcqs
from storage import save_text, get_text

load_dotenv()


UPLOAD_DIR = os.environ.get("UPLOAD_DIR", os.path.join(os.getcwd(), "data", "uploads"))
TEXT_DIR = os.environ.get("TEXT_DIR", os.path.join(os.getcwd(), "data", "texts"))
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")


os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)


app = Flask(__name__)
CORS(app)

@app.get("/api/health")
def health():
    return {"status": "ok", "model": DEFAULT_MODEL}

@app.post("/api/upload")
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No 'pdf' file part in request"}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400


    doc_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")
    text_path = os.path.join(TEXT_DIR, f"{doc_id}.txt")


    file.save(pdf_path)


    try:
        text, meta = extract_text_from_pdf(pdf_path)
        save_text(doc_id, text, text_path)
    except Exception as e:
        return jsonify({"error": f"Failed to extract text: {e}"}), 500
    
    return jsonify({
"doc_id": doc_id,
"pages": meta.get("pages"),
"chars": meta.get("chars"),
})

@app.post("/api/generate-quiz")
def make_quiz():
    data = request.get_json(silent=True) or {}
    doc_id = data.get("doc_id")
    n = int(data.get("num_questions", 8))
    model = data.get("model") or DEFAULT_MODEL


    if not doc_id:
        return jsonify({"error": "doc_id is required"}), 400


    text = get_text(doc_id, TEXT_DIR)
    if not text or len(text.strip()) == 0:
        return jsonify({"error": "No extracted text found for doc_id"}), 404


    try:
        quiz = generate_mcqs(text, n, model=model)
    except Exception as e:
        return jsonify({"error": f"Quiz generation failed: {e}"}), 500


    return jsonify({"questions": quiz})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)