🧠 Connecting the Dots — Round 1B
Challenge Objective
Transform a set of PDFs into an intelligent assistant for a specific persona performing a real-world task. The system should extract the most relevant content from each document and surface a ranked set of insights tailored to the persona's job to be done.

Solution Overview
Our solution performs persona-driven document intelligence by analyzing content relevance based on semantic similarity between the job description and document sections.

Key Components
Input JSON Parsing:

Reads the provided persona.json, which contains:

List of input PDFs

Persona description

Job to be done (task description)

PDF Processing:

Extracts all readable text from each PDF using PyMuPDF

Splits into coherent paragraph blocks with metadata

Embedding + Similarity:

Uses sentence-transformers (all-MiniLM-L6-v2, <90MB) to encode both:

Paragraphs from the PDF

Persona + job description as a query

Computes cosine similarity to rank the relevance of each paragraph

Ranking & Deduplication:

Top 5 relevant sections are selected

Paragraphs are deduplicated and reranked across documents

Final Output:

Produces a single structured JSON file with:

Metadata

Top 5 extracted sections

Subsection summaries

📦 File Structure
graphql
Copy
Edit
connecting-dots-round1b/

├── process_documents.py       # Main entry point

├── requirements.txt           # Dependencies

├── Dockerfile                 # AMD64 Docker build file

├── README.md                  # You’re reading it

├── input/

│   ├── persona.json           # Persona and task description

│   └── *.pdf                  # 3–10 PDF documents

└── output/
    └── output.json            # Final extracted summary
📁 Input / Output Format
🧾 Input:
One persona.json file in input/

Multiple .pdf files (3–10) also in input/

Example persona.json:
json
Copy
Edit
{
  "persona": { "role": "Travel Planner" },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  },
  "documents": [
    { "filename": "Cities.pdf", "title": "Cities of France" }
  ]
}
📤 Output:
A single file output.json in the output/ folder

Example output.json (structure):
json
Copy
Edit
{
  "metadata": {
    "input_documents": [...],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-07-20T14:00:00"
  },
  "extracted_sections": [
    {
      "document": "Cities.pdf",
      "section_title": "Top Cities for Youth Travel",
      "importance_rank": 1,
      "page_number": 4
    },
    ...
  ],
  "subsection_analysis": [
    {
      "document": "Cities.pdf",
      "refined_text": "Nice is vibrant and student-friendly, ideal for group visits...",
      "page_number": 4
    },
    ...
  ]
}
🚀 Docker Instructions
1. Build the Docker Image
bash
Copy
Edit
docker build --platform linux/amd64 -t round1b-solution:mytag .
2. Run the Container
Linux/macOS:

bash
Copy
Edit
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none round1b-solution:mytag
Windows CMD:

c
Copy
Edit
docker run --rm ^
  -v %cd%/input:/app/input ^
  -v %cd%/output:/app/output ^
  --network none round1b-solution:mytag
✅ Constraints Met
Constraint	Status
CPU-only	✅ Yes
Model size ≤ 1GB	✅ ~90MB used
Executes under 60s (5 PDFs)	✅
Offline / no internet	✅ Fully offline
Outputs valid structured JSON	✅

🔍 Sample Use Case
Persona: Travel Planner
Job to Be Done: Plan a 4-day trip for 10 college friends in the South of France.
Docs: 7 region-specific guides.

System Output:

Day-by-day highlights

Fun group activities

Relevant cuisine, accommodations, and safety tips

🧠 Libraries Used
PyMuPDF for PDF parsing

sentence-transformers for semantic similarity

scikit-learn, numpy, datetime, json, os
