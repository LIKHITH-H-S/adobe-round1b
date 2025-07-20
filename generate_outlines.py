import os
import json

# Set input/output directories
input_dir = "dataset/texts"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Simple heuristic for detecting headings
def is_heading(line):
    line = line.strip()
    if len(line) < 4 or len(line.split()) > 10:
        return False
    if line.isupper():
        return True
    if line.endswith(":"):
        return True
    return False

# Process each text file
for file in os.listdir(input_dir):
    if not file.endswith(".txt"):
        continue

    path = os.path.join(input_dir, file)
    outline = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if is_heading(line):
            outline.append({
                "level": "H3",
                "text": line.strip(),
                "page": i // 50 + 1  # Rough approximation of page
            })

    title = os.path.splitext(file)[0]
    structured = {
        "title": title,
        "outline": outline
    }

    output_path = os.path.join(output_dir, f"{title}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2)

print("✅ Outline extraction complete!")
