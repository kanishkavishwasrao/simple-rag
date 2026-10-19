"""Usage: python debug.py "your question" "keyword that must be in the answer chunk" """
import sys

from src.ingest import get_collection
from src.retriever import retrieve

if len(sys.argv) != 3:
    raise SystemExit('Usage: python debug.py "question" "keyword"')

question, keyword = sys.argv[1], sys.argv[2].lower()

# 1. Is the keyword in the index at all?
data = get_collection().get(include=["documents", "metadatas"])
matches = [
    (m["source"], m["chunk"])
    for d, m in zip(data["documents"], data["metadatas"])
    if keyword in d.lower()
]
print(f"Chunks containing '{keyword}': {matches}\n")

# 2. Where does it rank for the question?
for rank, c in enumerate(retrieve(question, k=50, rerank=False), 1):
    if keyword in c["text"].lower():
        print(f"First match at rank {rank} (score {c['score']})")
        print(c["text"][:500])
        break
else:
    print("Not in the top 50 results")