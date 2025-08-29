import os


def save_text(doc_id: str, text: str, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)




def get_text(doc_id: str, text_dir: str) -> str | None:
    path = os.path.join(text_dir, f"{doc_id}.txt")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()