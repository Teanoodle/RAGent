# RAGent

RAGent is a learning-focused project for building a traceable, multimodal Agentic RAG system step by step.

Phase 1 builds a general document intelligence foundation with multi-format ingestion, hybrid retrieval, reranking, retrieval routing, evidence-grounded answers, verification, and measurable evaluation. Phase 2 extends that foundation to financial news, filings, research reports, and quantitative text factors.

## Development principles

- Keep every milestone runnable, testable, explainable, and comparable.
- Preserve source locations so every answer can point back to its evidence.
- Support multiple formats through one format-neutral ingestion model.
- Design for text, tables, images, charts, and formulas without implementing every modality at once.
- Add agent behavior only when it solves a measurable problem.

## Current milestone

The repository currently contains:

- A runnable Python package and isolated virtual environment
- A format-neutral `SourceDocument` and `ContentBlock` model
- Modality labels for text, tables, images, charts, and formulas
- A page-aware PDF loader built on the shared ingestion model
- A line-aware TXT loader that preserves inclusive source line ranges
- Extension-based loader dispatch that can grow to support more formats
- A command that previews normalized document content
- Automated tests for loading, metadata, dispatch, errors, and the CLI

Currently implemented input formats:

- PDF files with an extractable text layer
- UTF-8 TXT files, including files with a UTF-8 byte-order mark

Planned input formats:

- DOCX
- HTML
- Markdown
- Scanned documents through OCR

Planned multimodal capabilities:

- Table extraction with source locations
- Embedded image extraction and captions
- Chart and diagram understanding through a vision-capable model
- Formula preservation and specialized extraction where practical

## Run the project

Requirements:

- Python 3.11 or newer

From the repository root, verify the default entry point:

```powershell
.\.venv\Scripts\python.exe -m ragent
```

Expected output:

```text
RAGent document ingestion is ready.
```

Inspect a supported document:

```powershell
.\.venv\Scripts\python.exe -m ragent inspect-document "data\raw\Attention is all you need.pdf" --max-chars 500
```

Inspect a plain-text document with line-range metadata:

```powershell
.\.venv\Scripts\python.exe -m ragent inspect-document "tests\fixtures\sample.txt" --max-chars 500
```

The earlier PDF-specific command remains available for compatibility:

```powershell
.\.venv\Scripts\python.exe -m ragent inspect-pdf "data\raw\Attention is all you need.pdf" --max-chars 500
```

## Run the tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Repository structure

```text
RAGent/
|-- AGENTS.md          # Persistent Codex instructions for future tasks
|-- data/
|   |-- indexes/       # Generated local indexes; contents are ignored by Git
|   `-- raw/           # Local source documents; contents are ignored by Git
|-- docs/
|   |-- CURRENT_STATUS.md  # Current implementation state and handoff guide
|   `-- ROADMAP.md         # Incremental implementation and learning plan
|-- ragent/
|   |-- documents/
|   |   |-- __init__.py
|   |   |-- errors.py
|   |   |-- loader.py
|   |   |-- models.py
|   |   |-- pdf_loader.py
|   |   `-- txt_loader.py
|   |-- __init__.py
|   |-- __main__.py
|   `-- cli.py
|-- tests/
|   |-- test_cli.py
|   |-- test_document_loader.py
|   |-- test_models.py
|   |-- test_pdf_loader.py
|   |-- test_txt_loader.py
|   |-- fixtures/
|   |   `-- sample.txt
|   `-- test_smoke.py
|-- .env.example
|-- .gitignore
|-- .worktreeinclude   # Ignored local files copied into managed worktrees
|-- pyproject.toml
`-- README.md
```

## Long-term pipeline

```text
Documents and web content
    -> Format-specific loaders
    -> SourceDocument and ContentBlock normalization
    -> Chunking
    -> Embedding and BM25 indexes
    -> Vector, BM25, or hybrid retrieval
    -> Reranking
    -> Query analysis and retrieval routing
    -> Evidence-grounded answer generation
    -> Critic and citation verification
    -> Evaluation and user interface
```
