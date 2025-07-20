import os
import json
from sentence_transformers import SentenceTransformer, util
import csv

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define query
query = "Graph Neural Networks for Drug Discovery"
query_embedding = model.encode(query, convert_to_tensor=True)

# Paths
input_dir = "output"
output_dir = "output_tables"
os.makedirs(output_dir, exist_ok=True)

top_sections = {}

# Process each JSON file
for file in os.listdir(input_dir):
    if not file.endswith(".json"):
        continue

    filepath = os.path.join(input_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if not isinstance(data.get("outline"), list):
                print(f"[SKIP] Invalid format (not a list): {filepath}")
                continue
        except Exception as e:
            print(f"[ERROR] Failed to parse {filepath}: {e}")
            continue

    sections = data["outline"]
    texts = [sec["text"] for sec in sections]
    embeddings = model.encode(texts, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, embeddings)[0].cpu().tolist()
    for i in range(len(sections)):
        sections[i]["score"] = scores[i]

    ranked = sorted(sections, key=lambda x: x["score"], reverse=True)[:5]
    top_sections[file] = ranked

# Print Results
for file, ranked in top_sections.items():
    print(f"\nTop sections in {file}:")
    for sec in ranked:
        print(f"  - {sec['text']} (Page {sec['page']}): {sec['score']:.4f}")

# ✅ Export to CSV
csv_path = os.path.join(output_dir, "section_rankings.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Section Title", "Page", "Score"])
    for file, ranked in top_sections.items():
        for sec in ranked:
            writer.writerow([file, sec["text"], sec["page"], f"{sec['score']:.4f}"])

# ✅ Export to HTML
html_path = os.path.join(output_dir, "section_rankings.html")
with open(html_path, "w", encoding="utf-8") as html:
    html.write("<html><head><title>Top Ranked Sections</title></head><body>")
    html.write("<h1>Top Sections from Research Papers</h1>")
    html.write("<table border='1' cellpadding='5'><tr><th>Filename</th><th>Section Title</th><th>Page</th><th>Score</th></tr>")
    for file, ranked in top_sections.items():
        for sec in ranked:
            html.write(f"<tr><td>{file}</td><td>{sec['text']}</td><td>{sec['page']}</td><td>{sec['score']:.4f}</td></tr>")
    html.write("</table></body></html>")

print("\n✅ Rankings exported to CSV and HTML!")
