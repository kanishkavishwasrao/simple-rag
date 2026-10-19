"""Streamlit UI.  Run:  streamlit run app.py"""
import streamlit as st

from src.config import DB_DIR
from src.ingest import build_index
from src.rag import ask

st.set_page_config(page_title="Simple RAG", page_icon="📚")
st.title("📚 Ask your documents")
st.caption("Retrieval-Augmented Generation · ChromaDB + Sentence-Transformers + Claude")

if not DB_DIR.exists():
    with st.spinner("Building index for the first time..."):
        n = build_index()
    st.success(f"Indexed {n} chunks")

question = st.text_input("Your question", placeholder="How many days of annual leave do employees get?")

if question:
    with st.spinner("Thinking..."):
        result = ask(question)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")
    for i, s in enumerate(result["sources"], 1):
        with st.expander(f"[{i}] {s['source']} · similarity {s['score']}"):
            st.write(s["text"])
