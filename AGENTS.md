# RAGent Project Instructions

## Project purpose

RAGent is a learning-focused, traceable, multimodal Agentic RAG project.

Phase 1 builds a general document intelligence foundation with multi-format ingestion, traceable chunking, vector and BM25 retrieval, hybrid retrieval, reranking, query routing, evidence-grounded generation, verification, evaluation, and a demonstration interface.

Phase 2 reuses that foundation for financial news, announcements, filings, research reports, and quantitative text-factor research.

## Required context before coding

Before starting a milestone:

1. Read `README.md`.
2. Read `docs/ROADMAP.md`.
3. Read `docs/CURRENT_STATUS.md`.
4. Inspect `git status` and preserve all existing user changes.
5. Inspect the relevant implementation and tests before editing.

## Communication and language

- Use English for source code, comments, docstrings, identifiers, tests, command output, configuration, and repository documentation.
- Explain work to the user in Chinese unless the user requests another language.
- Keep explanations suitable for a learner and define unfamiliar concepts.
- After coding, list every created and modified file and explain its purpose.
- Keep changes uncommitted until the user has reviewed and approved them.
- Do not push to GitHub unless the user explicitly approves the push.

## Implementation workflow

- Work in small, reviewable milestones.
- Prefer clear, framework-independent domain models and interfaces.
- Preserve source traceability through ingestion, chunking, retrieval, generation, and evaluation.
- Do not add agent loops or abstractions without a concrete problem and a measurable benefit.
- Do not overwrite unrelated user changes.
- Treat files under `data/raw/` as private, read-only source material.
- Do not add raw documents, generated indexes, secrets, or virtual environments to Git.

## Testing requirements

After every implementation change:

1. Run syntax or import validation.
2. Run the complete automated test suite.
3. Run focused tests for the changed behavior.
4. Run a real-document smoke test when a suitable local fixture is available.
5. Test expected error paths and invalid inputs.
6. Report each test or test group as passed or failed.
7. If any test fails, diagnose the cause, improve the implementation, and rerun both the focused test and the complete suite.
8. Run `git diff --check` before handoff.

Primary test command:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Current architecture

- `SourceDocument` stores document-level identity and metadata.
- `ContentBlock` stores traceable content and format-specific locations.
- `Modality` supports text, table, image, chart, and formula content.
- Format-specific loaders normalize source files into the shared models.
- `load_document()` dispatches to a loader by file extension.
- The CLI exposes `inspect-document`; `inspect-pdf` remains a compatibility alias.

Do not reintroduce a PDF-only domain model such as `DocumentPage`.

## Scope and sequence

- Follow the milestone order in `docs/ROADMAP.md`.
- Read `docs/CURRENT_STATUS.md` for the next recommended task.
- Build format-neutral ingestion before chunking.
- Build a measurable Classic RAG baseline before adding routing and verification agents.
- Design for multimodal content now, but implement OCR, table parsing, image extraction, and visual understanding in separate reviewable steps.

## Dependency and environment rules

- Use the project virtual environment at `.venv` when it exists.
- If `.venv` is absent, create it and install the project from `pyproject.toml`.
- Declare production dependencies in `pyproject.toml`.
- Explain why a new production dependency is needed before adding it.
- Do not store API keys in tracked files; use `.env` and keep `.env` ignored.
