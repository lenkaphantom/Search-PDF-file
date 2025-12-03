# 🕮 Project 2 — PDF Search Engine

This project implements a console-based search engine for a single PDF document. On startup the program parses the document pages (or loads already-parsed `txt/json` input), constructs data structures for efficient searching (trie, inverted index, page graph) and lets the user enter advanced text queries with ranked results.

Goal: provide fast and relevant search over the book "Data Structures and Algorithms in Python" (used as the test file), with a console menu, highlighted matches in context, and optional serialization to speed up subsequent runs.

**Quick overview**
- **Project name:** `Projekat2` — PDF search
- **Main entry:** `main.py`
- **Input:** PDF file (recommended) or pre-parsed `txt/json` (`parsed_text.json`)
- **Key modules:** `parsing_pdf.py`, `Trie.py`, `trie_serialization.py`, `Graph.py`, `graph_serialization.py`, `search.py`, `save_and_highlight_results.py`

**Features**
- **PDF parsing:** Extract text per page (`parsing_pdf.py`). If you prefer not to parse a PDF, use the provided `parsed_text.json`.
- **Trie:** Efficient per-page word lookup (`Trie.py`, `trie_serialization.py`).
- **Page graph:** Representation of links between pages inferred from references in the text (e.g. "See page 136") (`Graph.py`).
- **Ranking:** Scores consider occurrences of query terms on a page, occurrences on pages that link to it, and in-link counts (`search.py`).
- **Console menu:** Interactive menu for queries, pagination and extra options.
- **Serialization:** Save/load constructed structures to avoid rebuilding them every run (`trie_serialization.py`, `graph_serialization.py`).
- **Highlighting:** Option to create a PDF with the found keywords highlighted (`save_and_highlight_results.py`).

**Supported query features**
- Single or multiple words separated by spaces (ranked by frequency and presence).
- Logical operators: `AND`, `OR`, `NOT` (combine in expressions).
- Phrases in quotes (e.g. `"binary search"`) to match exact sequences.
- Autocomplete and wildcard support (e.g. `fun*`).

**Query examples**
- `python AND sequence`
- `dictionary NOT list`
- `"binary search"`
- `fun*` (autocomplete / suggestions)

**How to run (Windows / PowerShell)**
1. (Optional) Create a virtual environment and install dependencies if you use PDF libraries:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the program and follow the console menu:

```powershell
python main.py
```

Note: If there is no `requirements.txt`, recommended libraries for PDF parsing are `pdfminer.six` or `PyPDF2`. For colored console output consider `termcolor` or `colorama`.

**Repository structure**
- `main.py` — entry point and console menu
- `parsing_pdf.py` — parse PDF files into per-page text
- `Trie.py` — trie implementation
- `trie_serialization.py` — trie serialization / deserialization
- `Graph.py` — page graph representation and helpers
- `graph_serialization.py` — graph serialization / deserialization
- `search.py` — query parsing, ranking and result generation
- `save_and_highlight_results.py` — produce PDF with highlighted terms
- `parsed_text.json` — example of pre-parsed content (optional)
- `rezultati/` — directory for saved results and generated PDFs

**Grading mapping (how the project meets assignment criteria)**
- 10 points (basic requirements):
	- Results include result index, page number and a short context snippet.
	- Matches highlighted in the snippet (console color or markup).
	- Ranking based on term frequencies.
	- Multi-word queries influence the rank (more occurrences → higher rank).
	- Console menu to start searches.
- 17 points:
	- Ranking considers links (in-links) and occurrences on pages that link to the target page.
	- Pages organized as a graph (`Graph.py`).
	- Trie used for efficient per-page word lookup (`Trie.py`).
- 21 points:
	- Serialization of data structures for faster startup (`*_serialization.py`).
	- Support for logical operators `AND`, `OR`, `NOT` and pagination of results.
- >21 points (additional):
	- Phrase search, "did you mean" suggestions, operator grouping with parentheses and autocomplete.
	- Extra options such as extracting the first N result pages into a PDF and highlighting inside that PDF.
