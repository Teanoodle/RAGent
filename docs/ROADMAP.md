# RAGent Learning Roadmap

This roadmap develops a general, traceable Agentic RAG system before extending it to financial news and quantitative research.

## Phase 1: RAGent Core

### M0: Project foundation

Status: Completed.

Learning goals:

- Understand Python package structure, isolated environments, tests, and Git.
- Keep private source documents and generated indexes outside version control.

Acceptance criteria:

- The package runs with `python -m ragent`.
- Automated smoke tests pass.
- The repository is reproducible from its README.

### M1.1: Format-neutral ingestion model

Status: Completed.

Learning goals:

- Separate source identity from extracted content blocks.
- Represent format-specific locations without assuming every document has pages.
- Prepare for text, table, image, chart, and formula content.

Acceptance criteria:

- `SourceDocument` stores document-level identity and metadata.
- `ContentBlock` stores modality, content, and traceable source locations.
- The PDF loader returns the shared data model.
- Loader dispatch selects an implementation by file extension.

### M1.2: Multi-format text ingestion

Status: In progress. PDF and TXT are complete; Markdown is implemented and
awaiting review. DOCX and HTML remain planned.

Supported targets:

- PDF with an extractable text layer
- DOCX with headings and paragraph positions
- HTML with title, heading hierarchy, and source URL
- TXT with line ranges (implemented locally)
- Markdown with headings, prose, lists, and code blocks (implemented locally)

Acceptance criteria:

- One command inspects every supported local format.
- Every extracted block can be traced to a useful source location.
- Each loader has unit tests and at least one real-document smoke test.

### M1.3: Basic multimodal ingestion

Status: Planned.

Learning goals:

- Distinguish extracting an asset from understanding its meaning.
- Preserve relationships among text, captions, tables, and images.
- Use OCR only when normal text extraction is insufficient.

Planned output:

- Structured table blocks
- Extracted image assets and captions
- OCR fallback for scanned pages
- Page coordinates for PDF visual content
- A clear interface for later vision-model descriptions

### M1.4: Traceable chunking

Status: Planned.

Learning goals:

- Understand why retrieval uses chunks rather than complete documents.
- Compare fixed-size, heading-aware, and semantic chunking.
- Preserve document, section, page, line, and asset references.

Planned output:

- A deterministic `DocumentChunk` model and chunker
- Configurable chunk size and overlap
- Tests proving that all source metadata survives chunking

### M1.5: Basic vector RAG

Status: Planned.

Planned output:

- Replaceable embedding provider interface
- Local vector index
- Top-k semantic retrieval
- Evidence-grounded answers with source citations
- A small set of manually reviewed questions

### M2: Hybrid retrieval

Status: Planned.

Planned output:

- BM25 sparse retrieval
- Vector, BM25, and hybrid comparison modes
- Reciprocal Rank Fusion or a documented weighted fusion method
- Retrieval Recall@K, MRR, and nDCG@K measurements

### M3: Reranking

Status: Planned.

Planned output:

- A replaceable reranker interface
- Retrieval and reranking scores in inspection output
- An ablation comparison showing whether reranking improves results

### M4: Agentic retrieval routing

Status: Planned.

Planned output:

- Query analysis with structured decisions
- Explainable selection among vector, BM25, and hybrid retrieval
- Logged routing decisions and configurable top-k values
- A direct non-agent baseline for comparison

### M5: Critic and verifier

Status: Planned.

Planned output:

- Structured faithfulness and citation checks
- Unsupported-claim reporting
- Evidence-insufficiency handling
- Independent enable and disable controls for ablation tests

### M6: Benchmark and evaluation

Status: Planned.

Evaluation dimensions:

- Retrieval quality
- Answer correctness
- Faithfulness
- Citation precision and recall
- Latency
- Token and API cost

### M7: Demonstration interface

Status: Planned.

Planned output:

- Document upload and knowledge-base creation
- Questions and evidence-grounded answers
- Expandable source evidence
- Retrieval mode, reranker, agent, and critic controls
- Evaluation summaries suitable for demonstrations

## Phase 2: Financial research extension

Phase 2 reuses the ingestion, retrieval, routing, verification, and evaluation foundation instead of creating a separate project.

Planned sources:

- Financial news articles and local HTML archives
- Company announcements and regulatory filings
- Annual and quarterly reports
- Research reports
- Historical company and event context

Planned structured outputs:

- Entity and ticker mappings
- Event type, sentiment, novelty, attention, and impact signals
- Evidence-backed stock-by-date factor tables
- IC, ICIR, grouped-return, and long-short evaluations

## Scope control rule

Do not add a feature unless it answers both questions:

1. Which existing problem does it solve?
2. How will its improvement be measured?
