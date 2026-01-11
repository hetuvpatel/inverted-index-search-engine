#!/usr/bin/env python3
import argparse, os, json, time, sys

def load_dictionary(dict_path):
    terms = []
    dfs = []
    with open(dict_path, "r", encoding="utf-8") as f:
        for line in f:
            term, df = line.rstrip("\n").split("\t")
            terms.append(term); dfs.append(int(df))
    return terms, dfs

def load_postings(postings_path):
    term_to_postings = {}
    with open(postings_path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            term_to_postings[obj["term"]] = obj["postings"]
    return term_to_postings

def load_docs_meta(docs_jsonl):
    id2title = {}
    id2tokens = {}
    with open(docs_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            doc_id = obj["doc_id"]
            id2title[doc_id] = obj.get("title","")
            id2tokens[doc_id] = obj.get("text_tokens",[])
    return id2title, id2tokens

def snippet(tokens, pos, width=10, highlight="**"):
    start = max(0, pos - width)
    end = min(len(tokens), pos + width + 1)
    parts = tokens[start:pos] + [f"{highlight}{tokens[pos]}{highlight}"] + tokens[pos+1:end]
    return " ".join(parts)

def main():
    ap = argparse.ArgumentParser(description="Test inverted index (single-term query).")
    ap.add_argument("--index-dir", required=True)
    args = ap.parse_args()

    dict_path = os.path.join(args.index_dir, "dictionary.txt")
    postings_path = os.path.join(args.index_dir, "postings.txt")
    docs_jsonl = os.path.join(args.index_dir, "docs.jsonl")

    print("Loading index...")
    terms, dfs = load_dictionary(dict_path)
    term_to_postings = load_postings(postings_path)
    id2title, id2tokens = load_docs_meta(docs_jsonl)
    print(f"Loaded {len(terms)} terms. Type a term, or ZZEND to quit.")

    total_time = 0.0
    count = 0
    while True:
        try:
            q = input("> ").strip().lower()
        except EOFError:
            break
        if q == "ZZEND".lower():
            break
        t0 = time.time()
        postings = term_to_postings.get(q, [])
        df = len(postings)
        if df == 0:
            print(f"'{q}' not found.")
        else:
            print(f"Term: {q} | DF: {df}")
            for p in postings:
                doc_id = p["doc_id"]
                tf = p["tf"]
                positions = p["positions"]
                title = id2title.get(doc_id, "")
                print(f"- Doc {doc_id} | tf={tf} | title={title}")
                print(f"  positions: {positions}")
                # summary: first occurrence with 10-token context
                s = snippet(id2tokens[doc_id], positions[0], width=10, highlight='**')
                print(f"  summary: ... {s} ...")
        t1 = time.time()
        elapsed = (t1 - t0) * 1000.0
        total_time += elapsed; count += 1
        print(f"(Response time: {elapsed:.2f} ms)")
    if count > 0:
        print(f"Average response time: {total_time / count:.2f} ms")
    print("Bye.")

if __name__ == "__main__":
    main()
