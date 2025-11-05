# Simple Multimodal RAG System

A lightweight Retrieval-Augmented Generation system that can process and query text, image, and PDF files.

## Features

- Upload and process `.txt`, `.jpg`, `.png`, `.jpeg`, and `.pdf` files
- Extracts text using OCR (for images) or PDF parsing
- Stores embeddings and metadata in a Chroma vector database
- Query system retrieves the most relevant documents

## Tech Stack

- FastAPI (API backend)
- Sentence Transformers (Embeddings)
- Chroma (Vector store)
- PyMuPDF + Pytesseract (PDF & OCR extraction)

## Setup

```bash
git clone <your_repo_url>
cd <project_folder>
pip install -r requirements.txt
```
