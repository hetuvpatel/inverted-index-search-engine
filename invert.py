#!/usr/bin/env python3
import argparse, os, json, time
from utils import tokenize, load_stopwords, maybe_stem, parse_cacm_tar_gz

def build_index(docs, stopwords, do_stem):
    # term -> doc_id -> list[positions]
    index = {}
    docs_out = []
    for d in docs:
        doc_id = d["doc_id"]
        # Combine title + abstract into one token stream for positions
        combined_text = (d.get("title","") + " " + d.get("abstract","")).strip()
        tokens = []
        for tok in tokenize(combined_text):
            if tok in stopwords: 
                continue
            t = maybe_stem(tok, do_stem)
            tokens.append(t)
        # record positions per term
        pos_map = {}
        for i, t in enumerate(tokens):
            pos_map.setdefault(t, []).append(i)
        for t, pos in pos_map.items():
            index.setdefault(t, {})[doc_id] = pos
        docs_out.append({
            "doc_id": doc_id,
            "title": d.get("title",""),
            "text_tokens": tokens,  # for snippet and per-doc tf calculation
        })
    return index, docs_out

def write_outputs(index, docs_out, out_dir, meta):
    os.makedirs(out_dir, exist_ok=True)
    # dictionary and postings in aligned order
    terms = sorted(index.keys())
    dict_path = os.path.join(out_dir, "dictionary.txt")
    postings_path = os.path.join(out_dir, "postings.txt")
    with open(dict_path, "w", encoding="utf-8") as df, open(postings_path, "w", encoding="utf-8") as pf:
        for term in terms:
            postings = index[term]
            items = sorted(postings.items(), key=lambda kv: kv[0])  # sort by doc_id
            df.write(f"{term}\t{len(items)}\n")
            pf.write(json.dumps({
                "term": term,
                "postings": [{"doc_id": doc_id, "tf": len(pos), "positions": pos} for doc_id, pos in items]
            }, ensure_ascii=False) + "\n")
    with open(os.path.join(out_dir, "docs.jsonl"), "w", encoding="utf-8") as f:
        for d in docs_out:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return dict_path, postings_path

def main():
    ap = argparse.ArgumentParser(description="Build inverted index for CACM collection.")
    ap.add_argument("--input", required=True, help="Path to cacm.tar.gz")
    ap.add_argument("--stopwords", required=False, default=None, help="Path to stopwords.txt")
    ap.add_argument("--output-dir", required=True, help="Output directory")
    ap.add_argument("--stemming", choices=["on","off"], default="on")
    ap.add_argument("--stopwords_on", choices=["on","off"], default="on")
    args = ap.parse_args()

    t0 = time.time()
    docs = parse_cacm_tar_gz(args.input)
    stop = load_stopwords(args.stopwords) if args.stopwords_on == "on" else set()
    do_stem = (args.stemming == "on")
    index, docs_out = build_index(docs, stop, do_stem)
    dict_path, postings_path = write_outputs(index, docs_out, args.output_dir, {
        "stemming": do_stem, "stopwords_on": args.stopwords_on == "on",
        "stopwords_path": args.stopwords, "input": args.input, "docs": len(docs_out)
    })
    t1 = time.time()
    print(f"Built index for {len(docs_out)} docs in {t1 - t0:.2f}s")
    print(f"Dictionary: {dict_path}")
    print(f"Postings:   {postings_path}")
    print(f"Docs meta:  {os.path.join(args.output_dir, 'docs.jsonl')}")
    print(f"Meta:       {os.path.join(args.output_dir, 'meta.json')}")

if __name__ == "__main__":
    main()
