# Simple RAG: Ask Your Documents

A minimal, end-to-end Retrieval-Augmented Generation pipeline built from scratch (no LangChain), running fully locally: local embeddings, local vector DB, local LLM via Ollama. No API keys, no cost, no data leaving your machine.

## How it works

```
 Documents (.md/.txt/.pdf)
        │  chunk (400 words, 80 overlap)
        ▼
 Sentence-Transformers embeddings ──► ChromaDB (cosine similarity)
                                            │
 User question ──► embed ──► top-20 chunks ─┘
                                │
                                ▼
                 Cross-encoder reranker ──► top-6 chunks
                                │
                                ▼
              Prompt = system rules + chunks + question
                                │
                                ▼
              Ollama (llama3.2) answers only from context, cites sources
                                │
                                ▼
                       Answer + source chunks
```

Tech stack
Embeddings: all-MiniLM-L6-v2 (local, free)
Vector DB: ChromaDB (persistent, cosine)
Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2
LLM: llama3.2 running locally through Ollama
UI: Streamlit

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add your ANTHROPIC_API_KEY

python -m src.ingest        # build the index
streamlit run app.py        # web UI
python -m src.rag           # or use the CLI
python -m eval.evaluate     # retrieval hit-rate evaluation
```

Drop your own `.md`, `.txt` or `.pdf` files into `data/` and re-run `python -m src.ingest`.

## Design decisions
- **Grounded prompt:** the model must refuse when the context lacks the answer, which reduces hallucination.
- **Citations:** every answer references numbered sources, and the UI shows the raw chunks.
- **Overlapping chunks:** avoids cutting an answer in half at a chunk boundary.
- **Evaluation:** `eval/` measures retrieval hit rate so changes to chunk size or the embedding model can be compared with numbers, not guesses.

## Possible improvements
- Hybrid search (BM25 + vectors) and a cross-encoder reranker
- Semantic or heading-aware chunking
- Answer-quality evaluation (faithfulness, relevance) with an LLM judge
- Streaming responses and conversation memory
- Dockerfile and deployment
