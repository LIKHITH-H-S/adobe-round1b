## 🔍 Approach Explanation - Round 1B: Persona-Driven Document Intelligence

### 👤 Persona & Job-to-be-Done
Our solution is designed for a **PhD Researcher in Computational Biology** whose task is to **prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks** in the context of **Graph Neural Networks (GNNs) for Drug Discovery**.

---

### 🧠 Methodology

#### 1. Document Ingestion
We start by ingesting 4 research papers (`adb1.pdf`, `adb2.pdf`, `adb3.pdf`, and `adb4.pdf`) using `pdfjs-dist`, a lightweight and Node.js-compatible PDF parser.

#### 2. Outline Extraction
Using the `pdf.getOutline()` method, we extract all available section and sub-section titles from each document. These headings act as candidates for identifying relevant content.

#### 3. Section Relevance Ranking
For each document, we match outline entries against persona-specific goals using keyword mapping (`methodology`, `dataset`, `benchmark`, `evaluation`, `generation`, `interaction`, etc.). The most relevant sections are ranked from 1 to 8 globally based on:
- Term frequency of relevant keywords
- Section type (e.g., methods, results, evaluation)
- Contextual alignment with the researcher's job

#### 4. Sub-section Refinement
For every selected section, we extract a short refined summary (2–3 sentences) capturing the core idea. This ensures higher granularity for downstream tasks like summarization or Q&A.

---

### ⚙️ Runtime & Constraints
- ✅ **Runs on CPU-only** with no internet access
- ✅ **Model-free approach**; all logic is rule-based using document structure
- ✅ Processing time: **< 20 seconds** for 4 documents
- ✅ Model size: **< 1 GB** (no large dependencies used)

---

### 📦 Tools & Stack
- Node.js with `pdfjs-dist` for parsing outlines
- Docker for encapsulated execution
- JSON output generation for easy downstream usage

---

### 📈 Strengths & Future Scope
This approach is **generalizable**, **lightweight**, and **interpretable**, making it ideal for constrained environments. Future improvements could involve integrating lightweight ML models for better semantic matching and scoring.

