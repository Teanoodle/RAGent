# RAGent Learning Roadmap

This roadmap keeps implementation work small enough to understand and verify at every step.

## Step 0: Project foundation

Goal: create a clean, runnable, and version-controlled Python project.

Acceptance criteria:

- The package runs with `python -m ragent`.
- The smoke tests pass.
- Secrets, private documents, and generated indexes are ignored by Git.

## Step 1: Page-aware PDF loading

Learning goals:

- Understand how PDF text extraction works.
- Preserve document name and page number as metadata.
- Observe common extraction failures in technical PDFs.

Planned output:

- A loader that reads one PDF from `data/raw/`.
- A command that prints extracted text grouped by page.
- Unit tests for metadata and missing-file behavior.

## Step 2: Text chunking

Learning goals:

- Understand why retrieval operates on chunks instead of entire documents.
- Compare chunk size and overlap choices.

Planned output:

- A small `DocumentChunk` data model.
- A deterministic chunking function.
- Tests proving that page metadata survives chunking.

## Step 3: Embedding and vector retrieval

Learning goals:

- Understand embeddings and similarity search.
- Inspect retrieved evidence before adding answer generation.

Planned output:

- A local vector index.
- A top-k retrieval command.
- Search results containing text, document name, page number, and score.

## Step 4: Evidence-grounded answers

Learning goals:

- Build prompts from retrieved evidence.
- Separate unsupported model knowledge from document-supported claims.

Planned output:

- Answers generated only from retrieved evidence.
- Page-aware citations.
- A clear fallback when the evidence is insufficient.

## Step 5: Minimal web demo

Learning goals:

- Connect the tested RAG pipeline to a user interface.
- Keep UI code separate from retrieval logic.

Planned output:

- A Streamlit interface for document selection and questions.
- Expandable evidence cards showing source pages and chunks.

## Step 6: Baseline evaluation

Learning goals:

- Measure retrieval quality instead of relying on a few successful examples.
- Record failures before introducing more complex architecture.

Planned output:

- A small manually reviewed question set.
- Retrieval recall, latency, and citation checks.
- A baseline report used to evaluate later improvements.

