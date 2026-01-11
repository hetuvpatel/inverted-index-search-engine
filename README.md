# inverted-index-search-engine

# Inverted Index Construction and Search System  
**CPS842: Information Retrieval and Web Search – Assignment 1 (Fall 2025)**

This project implements a complete **information retrieval pipeline** for building and querying an **inverted index** from a large document collection. Using the CACM (Communications of the ACM) dataset, the system supports efficient term-based search with positional indexing, optional stop-word removal, stemming, and interactive query evaluation with performance measurement.

---

## 📌 Project Overview

The system consists of two main components:

1. **Index Construction (`invert`)**
   - Parses a document collection
   - Builds an inverted index with positional information
   - Outputs a dictionary file and a postings list file

2. **Index Querying (`test`)**
   - Loads the generated index
   - Supports interactive term search
   - Displays detailed document-level results and query timing

This project demonstrates core concepts in **Information Retrieval**, including indexing, text preprocessing, and efficient query processing.

---

## 📂 Dataset

- **Collection:** CACM (Communications of the ACM)
- **Documents:** 3,204
- **Fields used:**
  - `.I` – Document ID
  - `.T` – Title
  - `.W` – Abstract
  - `.B` – Publication date
  - `.A` – Authors
- **Indexed content:** Title and Abstract
- **Vocabulary size:** ~10,446 terms

---

## ⚙️ Features

### Inverted Index
- Alphabetically sorted dictionary
- One-to-one mapping between dictionary terms and postings lists
- Each posting includes:
  - Document ID
  - Term frequency
  - Positions of all occurrences in the document

### Text Processing (Configurable)
- Stop-word removal (using provided CACM stopword list or `stopwords.txt`)
- Stemming (Porter Stemmer)
- Both components can be **enabled or disabled at runtime**

### Interactive Search
- Query a single term at a time
- Displays:
  - Document frequency
  - Matching document IDs
  - Term frequency per document
  - Positional information
  - Document title
  - Contextual summary (±10 terms around first occurrence)
- Special command `ZZEND` terminates the program

### Performance Measurement
- Measures time taken per query
- Outputs average query response time on exit

---

## 🧠 Algorithms & Data Structures

- **Dictionary:** HashMap / TreeMap (for fast lookup and sorted output)
- **Postings List:** Ordered lists indexed by document ID
- **Indexing Strategy:** Single-pass inverted index construction
- **Search Strategy:** Direct dictionary lookup with sequential postings traversal
- **Stemming:** Porter Stemming Algorithm

---


