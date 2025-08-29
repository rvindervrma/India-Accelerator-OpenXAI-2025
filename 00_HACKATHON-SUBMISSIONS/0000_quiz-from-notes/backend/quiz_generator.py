import json
import re
from textwrap import dedent
from ollama_client import OllamaClient

SYSTEM_PROMPT = dedent(
    """
    You are a strict MCQ generator for student revision. Given academic notes text,
    you must produce ONLY a compact JSON array named `questions` where each item is:
    {
    "question": string,
    "options": [string, string, string, string],
    "answer": string,
    "explanation": string
    }
    Rules:
    - 4 options per question, exactly one correct.
    - Keep questions concise but clear.
    - Ensure the correct answer is one of the options.
    - Output ONLY JSON (no markdown, no commentary).
    """
)

USER_PROMPT_TEMPLATE = dedent(
    """
    Generate {n} MCQs based strictly on the following notes text.
    Use only facts present in the text; do not invent content.

    Notes:
    ---
    {content}
    ---

    Return JSON ONLY.
    """
)

def _coerce_json_array(s: str):
    match = re.search(r"\[.*\]", s, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON array found in model response")
    raw = match.group(0)
    return json.loads(raw)

def generate_mcqs(text: str, n: int = 8, model: str = "llama3.1:8b"):
    
    client = OllamaClient(model)
    prompt = USER_PROMPT_TEMPLATE.format(n=n, content=text[:20000])  # truncate large text
    
    # Call the model safely
    try:
        raw = client.generate_json(prompt, system=SYSTEM_PROMPT)
    except Exception as e:
        return {"error": f"Failed to generate MCQs: {e}"}

    # Parse model response safely
    try:
        arr = _coerce_json_array(raw)
    except Exception as e:
        try:
            obj = json.loads(raw)
            arr = obj.get("questions", [])
            if not isinstance(arr, list):
                raise ValueError("'questions' key is not a list")
        except Exception as e2:
            return {"error": f"Failed to parse JSON from model: {e2}"}

    # Validate and clean questions
    cleaned = []
    for i, q in enumerate(arr):
        try:
            question = str(q.get("question", "")).strip()
            options = q.get("options", [])
            answer = str(q.get("answer", "")).strip()
            explanation = str(q.get("explanation", "")).strip()

            if not question or not isinstance(options, list) or len(options) != 4:
                continue

            options = [str(o).strip() for o in options]
            if answer not in options:
                options = [answer] + [o for o in options if o != answer]
                options = options[:4] if len(options) >= 4 else (options + ["N/A"] * (4 - len(options)))

            cleaned.append({
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation or ""
            })
        except Exception as qe:
            continue

    return cleaned[:n] if cleaned else {"error": "No valid questions generated"}
