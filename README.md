# RAGent

**A traceable, multimodal Agentic RAG foundation for financial news understanding and quantitative research.**

RAGent is a learning-focused project that develops a general document intelligence system first, then extends it into a financial research pipeline. Its long-term goal is to turn unstructured news, filings, announcements, and research reports into evidence-backed, testable quantitative signals.

This repository is being built incrementally. The current implementation provides the document-ingestion foundation; retrieval, agents, financial signal generation, and backtesting are planned milestones rather than completed features.

## Why this project?

A traditional RAG system usually retrieves documents and asks a language model to answer a question:

```text
Question -> Retrieval -> LLM -> Answer
```

Financial news analysis requires a stricter and more measurable workflow. A useful system should identify the affected companies, classify the event, distinguish text sentiment from likely market impact, find comparable historical events, preserve the supporting evidence, and test whether the resulting signal has predictive value.

RAGent therefore targets the following end-to-end research loop:

```text
Financial documents and news
    -> Traceable ingestion
    -> Cleaning and deduplication
    -> Entity and event extraction
    -> Hybrid retrieval of historical evidence
    -> Evidence-grounded financial analysis
    -> Structured news signals
    -> Factor construction
    -> Backtesting and evaluation
```

The project does not treat an LLM as a black-box stock predictor. The intended division of responsibilities is:

```text
LLM and retrieval:       extraction, evidence retrieval, reasoning, tool selection
Quantitative research:   signal construction, statistical validation, backtesting
```

## Current status

RAGent is currently in **Phase 1: document intelligence foundation**, milestone **M1.2: multi-format text ingestion**.

Implemented today:

- A format-neutral `SourceDocument` and `ContentBlock` data model
- Traceable content locations using pages, sections, paragraphs, and line ranges
- Modality labels for text, tables, images, charts, and formulas
- Page-aware PDF loading for documents with an extractable text layer
- Line-aware UTF-8 TXT loading, including UTF-8 byte-order marks
- Structure-aware Markdown loading for headings, prose, lists, and fenced code blocks
- Extension-based loader dispatch through `load_document()`
- A shared CLI for inspecting normalized document content
- Automated tests for models, loaders, dispatch, error handling, and CLI behavior

Not implemented yet:

- DOCX and HTML ingestion
- OCR, table parsing, embedded image extraction, and visual understanding
- Chunking, embeddings, vector search, BM25, and hybrid retrieval
- Reranking, query routing, answer generation, and citation verification
- Financial entity linking, event classification, sentiment, and novelty scoring
- Market data integration, factor construction, and backtesting
- A web API or demonstration interface

Keeping these boundaries explicit makes each future improvement measurable and prevents planned architecture from being mistaken for working software.

## Traceability-first design

Every normalized content block carries its source identity and the most useful location available for its format. For example:

- PDF content retains page numbers.
- TXT content retains inclusive line ranges.
- Markdown content retains line ranges, heading paths, and structural metadata.

This traceability is intended to survive later chunking, retrieval, generation, and evaluation so that an answer or financial signal can be inspected back to its original evidence.

The shared model is also format-neutral: RAGent does not use a PDF-only domain model. This allows future loaders and modalities to enter the same downstream pipeline.

## Quick start

### Requirements

- Python 3.11 or newer
- PowerShell for the commands below

### Set up the environment

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

Verify the package entry point:

```powershell
.\.venv\Scripts\python.exe -m ragent
```

Expected output:

```text
RAGent document ingestion is ready.
```

### Inspect a document

Use the same command for every supported format:

```powershell
.\.venv\Scripts\python.exe -m ragent inspect-document "path\to\document.pdf" --max-chars 500
```

Examples using the tracked test fixtures:

```powershell
.\.venv\Scripts\python.exe -m ragent inspect-document "tests\fixtures\sample.txt" --max-chars 500
.\.venv\Scripts\python.exe -m ragent inspect-document "tests\fixtures\sample.md" --max-chars 500
```

The earlier PDF-specific command remains available as a compatibility alias:

```powershell
.\.venv\Scripts\python.exe -m ragent inspect-pdf "path\to\document.pdf" --max-chars 500
```

## Run the tests

Run the complete automated suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The test suite covers successful loading, source metadata, loader dispatch, invalid inputs, and CLI behavior.

## Architecture

The implementation is intentionally staged. Later stages will be added only after the preceding baseline is testable.

```text
Current foundation
------------------
PDF / TXT / Markdown
    -> Format-specific loaders
    -> SourceDocument + ContentBlock
    -> Traceable normalized content

General RAG foundation
----------------------
Normalized content
    -> Traceable chunking
    -> Vector and BM25 indexes
    -> Hybrid retrieval
    -> Reranking
    -> Evidence-grounded generation
    -> Citation and faithfulness verification
    -> Retrieval and answer evaluation

Financial research extension
----------------------------
News / filings / announcements / reports
    -> Entity and ticker linking
    -> Event classification
    -> Sentiment, novelty, relevance, and impact analysis
    -> Historical-event and market-reaction retrieval
    -> Structured signals
    -> Factor aggregation
    -> Backtesting and statistical evaluation
```

## Target financial signal

A later financial event pipeline may produce a structured record such as:

```json
{
  "timestamp": "2026-09-25T09:31:00Z",
  "ticker": "NVDA",
  "event_type": "product_pricing",
  "sentiment": -0.42,
  "impact": 0.78,
  "novelty": 0.71,
  "relevance": 0.96,
  "historical_impact": -0.55,
  "confidence": 0.87,
  "evidence_ids": ["document-id:block-id"]
}
```

This is a target schema, not current CLI output. Its important property is that numerical scores remain linked to inspectable evidence.

A simple research baseline could combine these values as:

```text
NewsSignal = Sentiment x Impact x Novelty x Relevance x Confidence
```

More advanced experiments may add historical impact, source reliability, time decay, market regime, and event-specific weights. Each addition should be compared with a simpler baseline rather than assumed to improve performance.

## Evaluation philosophy

Complexity is useful only when it produces a measurable improvement. Planned experiments will compare increasingly capable systems, for example:

1. Financial sentiment only
2. Sentiment with time decay
3. LLM-based structured extraction
4. LLM extraction with historical RAG
5. Agentic retrieval with novelty, impact, and market context

Evaluation will cover both information retrieval and quantitative research:

- Retrieval: Recall@K, MRR, nDCG@K, and reranking gain
- Generation: correctness, faithfulness, citation precision, and citation recall
- Classification: entity, ticker, event type, and sentiment accuracy
- Factors: Pearson IC, Rank IC, ICIR, quantile returns, long-short returns, turnover, Sharpe ratio, and drawdown
- Operations: latency, token usage, and API cost

Timestamp handling will be part of the data model. The pipeline must distinguish `published_at`, signal availability, trade time, and return horizon to avoid look-ahead bias.

## Roadmap

The project follows small, reviewable milestones:

- **M0 — Foundation:** package structure, isolated environment, tests — complete
- **M1.1 — Shared ingestion model:** format-neutral, traceable document blocks — complete
- **M1.2 — Multi-format text ingestion:** PDF and TXT complete; Markdown awaiting review; DOCX and HTML planned
- **M1.3 — Multimodal ingestion:** tables, images, OCR, charts, and formulas
- **M1.4 — Traceable chunking:** deterministic chunks with preserved source metadata
- **M1.5 — Classic vector RAG:** embeddings, local index, retrieval, and cited answers
- **M2 — Hybrid retrieval:** BM25, vector search, fusion, and retrieval metrics
- **M3 — Reranking:** replaceable reranker and ablation measurements
- **M4 — Agentic routing:** explainable retrieval decisions with a non-agent baseline
- **M5 — Critic and verifier:** faithfulness, citation, and insufficient-evidence checks
- **M6 — Benchmarking:** quality, latency, token, and cost evaluation
- **M7 — Demonstration interface:** document upload, evidence inspection, and experiment controls
- **Phase 2 — Financial research:** news understanding, structured signals, factor construction, and backtesting

See [docs/ROADMAP.md](docs/ROADMAP.md) for acceptance criteria and [docs/CURRENT_STATUS.md](docs/CURRENT_STATUS.md) for the latest handoff state.

## Repository structure

```text
RAGent/
|-- ragent/
|   |-- documents/
|   |   |-- models.py           # Shared document and content-block models
|   |   |-- loader.py           # Extension-based loader dispatch
|   |   |-- pdf_loader.py       # Page-aware PDF ingestion
|   |   |-- txt_loader.py       # Line-aware TXT ingestion
|   |   |-- markdown_loader.py  # Structure-aware Markdown ingestion
|   |   `-- errors.py           # Shared ingestion errors
|   |-- cli.py                  # inspect-document command
|   `-- __main__.py             # python -m ragent entry point
|-- tests/                      # Automated tests and text fixtures
|-- data/
|   |-- raw/                    # Private local source material; ignored by Git
|   `-- indexes/                # Generated local indexes; ignored by Git
|-- docs/
|   |-- ROADMAP.md              # Milestones and acceptance criteria
|   `-- CURRENT_STATUS.md       # Current implementation and next task
|-- pyproject.toml
`-- README.md
```

## Development principles

- Keep every milestone runnable, testable, explainable, and comparable.
- Preserve source traceability through ingestion, retrieval, generation, and evaluation.
- Build a measurable Classic RAG baseline before adding agent loops.
- Separate text sentiment from estimated market impact.
- Treat raw documents as private, read-only source material.
- Keep generated indexes, secrets, and virtual environments out of Git.
- Add a feature only when it solves a concrete problem and its benefit can be measured.

## Research questions

The financial extension is designed to test questions such as:

- Does historical-event retrieval improve post-news return analysis?
- Does novelty-adjusted sentiment outperform raw sentiment?
- Does event-specific analysis outperform general sentiment classification?
- Does LLM-based impact scoring add information beyond a financial sentiment baseline?
- How quickly does the predictive value of different news events decay?
- Does agentic retrieval improve signal quality enough to justify its additional cost and complexity?

## Disclaimer

RAGent is intended for education and research. It is not financial advice and is not intended for live trading or investment decision-making.
