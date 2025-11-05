from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uuid
import datetime

from utils.extractors import extract_content
from utils.embeddings import embed_text
from utils.storage import get_collection
from utils.llm import generate_answer

app = FastAPI(title="Simple MultiModal RAG system")

app.mount("/static", StaticFiles(directory="static"), name = "static")

collection = get_collection("docs")

@app.get("/", response_class = HTMLResponse)
async def home():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_file(file : UploadFile):
    content = await extract_content(file)
    if not content.strip():
        return {"error" : "No readable content found"}

    embeddings  = embed_text(content)
    metadata = {
        "filename" : file.filename,
        "timestamp" : datetime.datetime.now().isoformat(),
        "file_type" : file.content_type,
    }

    doc_id = str(uuid.uuid4())

    collection.add(
        ids = [doc_id],
        documents = [content],
        embeddings = [embeddings],
        metadata = [metadata],
    )

    return {"message" : f"{file.filename} uploaded and stored", "metadata" : metadata}

@app.post("/query")
async def query_endpoint(query: str = Form(...)):
    query_embedding = embed_text(query)
    results = collection.query(query_embedding = [query_embedding], n_results = 3)
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    context = "\n\n".join(docs)

    answer = generate_answer(query, context)

    return {
        "query" : query,
        "answer" : answer,
        "retrieved" : [
            {"document" : d, "metadata" : m} for d, m in zip(docs, metadatas)
        ]
    }

@app.get("/health")
async def health():
    return {"status" : "ok"}
 



