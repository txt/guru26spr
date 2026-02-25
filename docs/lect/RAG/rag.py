import os, io, hashlib, pickle, faiss, argparse, warnings, numpy as np
from pathlib import Path
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import requests
from pathlib import Path
from PyPDF2 import PdfReader

warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"   # fixes segfault on macOS

PDF_DIR     = "docs"
PAGE_FILE   = "page.file"
CHUNK_WORDS = 180   # ≈ short paragraph (150–220 works well)
TOPK        = 6     # sensible default (5–8)
EMBED_BATCH = 64    # larger batches = faster GPU/CPU throughput

model = SentenceTransformer("all-MiniLM-L6-v2")

def file_sig(path):
    p=Path(path); h=hashlib.md5()
    h.update(str(p.stat().st_mtime_ns).encode()); h.update(str(p.stat().st_size).encode())
    return h.hexdigest()

def load_texts_with_meta(pdf_path):  # -> list[(text, meta)] where meta has doc/page
    out=[]; p=Path(pdf_path)
    try:
        reader = PdfReader(str(p))
        for i, pg in enumerate(reader.pages, start=1):
            t = pg.extract_text() or ""
            if t.strip():
                out.append((t, {"doc": p.name, "page": i}))
    except Exception as e:
        print(f"warn: failed to read {p}: {e}")
    return out

def chunk_text(text, n=CHUNK_WORDS):
    w=text.split(); return [" ".join(w[i:i+n]) for i in range(0,len(w),n)]

def build_chunks(pdf_dir):
    chunks, metas = [], []
    for pdf in Path(pdf_dir).glob("*.pdf"):
        for t, meta in load_texts_with_meta(pdf):
            cs = chunk_text(t)
            chunks.extend(cs)
            metas.extend([{**meta, "chunk": j+1} for j in range(len(cs))])
    return chunks, metas
    
def encode(arr):
    return np.asarray(model.encode(arr, convert_to_numpy=True,
                                   batch_size=EMBED_BATCH,
                                   show_progress_bar=len(arr) > 200), dtype="float32")

def build_index(chunks):
    X = encode(chunks)
    ix = faiss.IndexFlatL2(X.shape[1])  # squared L2 distance
    ix.add(X)
    return ix, X

def save_pagefile(ix, X, chunks, metas, manifest, path=PAGE_FILE):
    with open(path, "wb") as f:
        pickle.dump({"ix": ix, "X": X, "chunks": chunks, "metas": metas,
                     "manifest": manifest}, f)

def load_pagefile(path=PAGE_FILE):
    with open(path, "rb") as f: return pickle.load(f)

# Build fresh (first run)

def build_pagefile(pdf_dir=PDF_DIR, path=PAGE_FILE):
    chunks, metas = build_chunks(pdf_dir)
    ix, X = build_index(chunks)
    manifest = {str(p): file_sig(p) for p in Path(pdf_dir).glob("*.pdf")}
    save_pagefile(ix, X, chunks, metas, manifest, path)
    return ix, X, chunks, metas, manifest

# Update (incremental add/modify). If deletions detected → rebuild for simplicity.

def update_pagefile(pdf_dir=PDF_DIR, path=PAGE_FILE):
    if not os.path.exists(path):
        return build_pagefile(pdf_dir, path)
    pf = load_pagefile(path)
    old_manifest = pf["manifest"]
    current = {str(p): file_sig(p) for p in Path(pdf_dir).glob("*.pdf")}

    deleted = set(old_manifest) - set(current)
    added_or_changed = [p for p,s in current.items() if old_manifest.get(p) != s]

    if deleted:
        # IndexFlatL2 lacks easy deletions; simplest: full rebuild to stay correct.
        return build_pagefile(pdf_dir, path)

    if not added_or_changed:
        return pf["ix"], pf["X"], pf["chunks"], pf["metas"], current

    # Append new/changed content
    new_chunks, new_metas = [], []
    for p in added_or_changed:
        for t, meta in load_texts_with_meta(p):
            cs = chunk_text(t)
            new_chunks.extend(cs)
            new_metas.extend([{**meta, "chunk": j+1} for j in range(len(cs))])

    if new_chunks:
        X_new = encode(new_chunks)
        pf["ix"].add(X_new)
        pf["X"] = np.vstack([pf["X"], X_new])
        pf["chunks"].extend(new_chunks)
        pf["metas"].extend(new_metas)

    pf["manifest"] = current
    save_pagefile(pf["ix"], pf["X"], pf["chunks"], pf["metas"], pf["manifest"], path)
    return pf["ix"], pf["X"], pf["chunks"], pf["metas"], pf["manifest"]
    
OLLAMA_URL = "http://localhost:11434/api/chat"
LLM_MODEL  = "llama3.2"   # run: ollama pull llama3.2

def query_rag(query, index, chunks, k=TOPK):
    qvec = encode([query])
    D, I = index.search(qvec, k)           # D: squared distances, I: indices
    retrieved = [chunks[i] for i in I[0]]
    context = "\n\n".join(retrieved)
    prompt = (f"Answer the question based only on the context below.\n\n"
              f"Context:\n{context}\n\nQuestion: {query}\nAnswer:")
    resp = requests.post(OLLAMA_URL, json={
        "model":    LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream":   False
    }, timeout=60)
    rjson = resp.json()
    if "message" not in rjson:
        raise RuntimeError(f"Ollama error: {rjson}")
    return rjson["message"]["content"].strip(), list(zip(D[0].tolist(), I[0].tolist()))


### 6) Helper: print a Semantic Page Table (auditability)

def show_page_table(chunks, metas, scores):
    print("# Semantic Page Table (top-k)")
    for r,(d, idx) in enumerate(scores, 1):
        m = metas[idx]
        snip = chunks[idx][:80].replace('\n',' ')
        print(f"{r:>2}. idx={idx:>6}  L2^2={d:.4f}  {m['doc']}#p{m['page']}  '{snip}'")


### 7) Main entrypoints

def ensure_pagefile(rebuild=False):
    if rebuild and os.path.exists(PAGE_FILE):
        os.remove(PAGE_FILE)
    return update_pagefile(PDF_DIR, PAGE_FILE)

def run_query(q, ix, chunks, metas):
    print(f"\n[rag] query: {q!r}", flush=True)
    ans, scores = query_rag(q, ix, chunks, k=TOPK)
    show_page_table(chunks, metas, scores)
    print(f"\n---\n{ans}")

def read_multiline(prompt="> "):
    """End a line with \\ to continue on the next line. 'quit' to exit."""
    print(prompt, end="", flush=True)
    lines = []
    while True:
        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            return None
        if not lines and line.strip().lower() in ("quit", "exit", "q"):
            return None
        if line.endswith("\\"):
            lines.append(line[:-1])
            print("... ", end="", flush=True)
        else:
            lines.append(line)
            break
    return " ".join(lines).strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic Paging RAG")
    parser.add_argument("--query",   type=str,           help="Single question to ask")
    parser.add_argument("--rebuild", action="store_true", help="Force full rebuild of page.file")
    parser.add_argument("--repl",    action="store_true", help="Interactive multiline question loop")
    args = parser.parse_args()

    ix, X, chunks, metas, manifest = ensure_pagefile(rebuild=args.rebuild)
    print(f"[rag] index ready — {len(chunks)} chunks, {ix.ntotal} vectors")

    if args.query:
        run_query(args.query, ix, chunks, metas)

    if args.repl or not args.query:
        print("\n[rag] REPL — enter your question (end a line with \\ to continue)")
        print("      type 'quit' to exit\n")
        while True:
            q = read_multiline("> ")
            if q is None:
                break
            if q:
                run_query(q, ix, chunks, metas)