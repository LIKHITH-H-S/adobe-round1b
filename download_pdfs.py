import arxiv
import os

# Define search query and number of papers
query = "Graph Neural Networks drug discovery"
max_results = 50

# Output directory
output_dir = "dataset/pdfs"
os.makedirs(output_dir, exist_ok=True)

# Search and download
search = arxiv.Search(
    query=query,
    max_results=max_results,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

for result in search.results():
    paper_title = result.title.replace("/", "_").replace(":", "_")
    filename = f"{paper_title}.pdf"
    pdf_path = os.path.join(output_dir, filename)

    try:
        print(f"Downloading: {result.title}")
        result.download_pdf(dirpath=output_dir, filename=filename)
    except Exception as e:
        print(f"Failed to download {result.title}: {e}")

print("✅ Done downloading all papers!")
