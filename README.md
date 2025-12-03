# 🕮 PDF Search Engine

This project implements a console-based search engine for a single PDF document. On startup the program parses the document pages (or loads already-parsed `txt/json` input), constructs data structures for efficient searching (trie, inverted index, page graph) and lets the user enter advanced text queries with ranked results.

Goal: provide fast and relevant search over the book "Data Structures and Algorithms in Python" (used as the test file), with a console menu, highlighted matches in context, and optional serialization to speed up subsequent runs.

**Quick overview**
- **Project name:** PDF search
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
	- Serialization of data structures for faster startup (`*_serialization.py`).
	- Support for logical operators `AND`, `OR`, `NOT` and pagination of results.
