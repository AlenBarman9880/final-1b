import os
import json
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util
from datetime import datetime

# Load the embedding model (under 200MB for compliance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_persona(file_path=r"C:\Users\KIIT\OneDrive\Documents\connecting-dots-round1b\input\challenge1b_input.json"):
    """Reads the persona and job-to-be-done from the input JSON format provided."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    persona = data["persona"]["role"]
    job = data["job_to_be_done"]["task"]
    return f"{persona}: {job}", {
        "persona": persona,
        "job": job,
        "challenge_info": data.get("challenge_info", {}),
        "documents": data.get("documents", [])
    }


def extract_paragraphs_from_pdf(pdf_path):
    """Extracts paragraphs from a PDF document."""
    doc = fitz.open(pdf_path)
    paragraphs = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if len(text) > 50 and not text.lower().startswith("page "):
                paragraphs.append({
                    "text": text,
                    "page": page_num
                })
    return paragraphs


def rank_paragraphs(paragraphs, query, top_k=5):
    """Ranks paragraphs by semantic similarity to the query."""
    texts = [p["text"] for p in paragraphs]
    para_embeddings = model.encode(texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(query_embedding, para_embeddings)[0]
    ranked = sorted(zip(texts, [p["page"] for p in paragraphs], scores),
                    key=lambda x: x[2], reverse=True)

    results = []
    for i, (text, page, score) in enumerate(ranked[:top_k]):
        results.append({
            "document": "",  # will fill this later
            "page_number": page,
            "section_title": text[:60] + "..." if len(text) > 60 else text,
            "importance_rank": i + 1,
            "refined_text": text
        })
    return results


def process_all_pdfs(input_dir="input", output_dir="output"):
    query, meta = load_persona(os.path.join(input_dir, r"C:\Users\KIIT\OneDrive\Documents\connecting-dots-round1b\input\challenge1b_input.json"))

    results = []
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        paragraphs = extract_paragraphs_from_pdf(pdf_path)
        ranked = rank_paragraphs(paragraphs, query)

        for r in ranked:
            r["document"] = pdf_file
            results.append(r)

    output = {
        "metadata": {
            "input_documents": pdf_files,
            "persona": meta["persona"],
            "job_to_be_done": meta["job"],
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": results
    }

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "result.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    process_all_pdfs()
