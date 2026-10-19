# simple-rag
A from-scratch RAG pipeline: drop in .md, .txt or .pdf files and ask questions in plain English. Answers come strictly from your documents, with sources cited. Files are split into overlapping 120-word chunks, embedded locally with all-MiniLM-L6-v2, and stored in a persistent ChromaDB index.
