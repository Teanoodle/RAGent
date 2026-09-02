# RAGent

RAGent is a learning-focused project for building a traceable technical-document question-answering system step by step.

The project starts with a small Classic RAG baseline. More advanced retrieval, agent, verification, and multimodal features will only be added after the baseline is measurable and stable.

## Current milestone

The repository currently contains only the initial Python project scaffold.

Completed:

- A runnable Python package
- A smoke test
- Local data directories that do not commit private documents or generated indexes
- A staged roadmap for the first Classic RAG baseline

Not implemented yet:

- PDF parsing
- Chunking
- Embeddings
- Vector retrieval
- LLM answer generation
- Web interface

## Run the project

Requirements:

- Python 3.11 or newer

From the repository root, run:

```powershell
python -m ragent
```

Expected output:

```text
RAGent is ready for the V0 implementation.
```

## Run the tests

```powershell
python -m unittest discover -s tests -v
```

## Repository structure

```text
RAGent/
├── data/
│   ├── indexes/       # Generated local indexes; contents are ignored by Git
│   └── raw/           # Local source documents; contents are ignored by Git
├── docs/
│   └── ROADMAP.md     # Incremental learning and implementation plan
├── ragent/
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py
├── tests/
│   └── test_smoke.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Development principle

Every milestone should remain runnable, testable, explainable, and comparable with the previous milestone.

