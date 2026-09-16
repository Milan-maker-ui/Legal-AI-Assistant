from pathlib import Path

from fastapi import FastAPI, HTTPException

from app.models.schemas import (
    QuestionRequest,
    AnswerResponse,
    Source
)

from app.ingestion.loader import (
    load_pdf
)

from app.ingestion.chunking import (
    create_chunks
)

from app.ingestion.embeddings import (
    create_embeddings
)

from app.retrieval.vector_store import (
    VectorStore
)

from app.retrieval.retriever import (
    Retriever
)

from app.llm.generator import (
    generate_answer
)


# ==================================================
# CREATE FASTAPI APP
# ==================================================

app = FastAPI(
    title="Legal AI Assistant",
    description="RAG-based Legal Document Question Answering System",
    version="1.0.0"
)


# ==================================================
# GLOBAL VARIABLES
# ==================================================

vector_store = VectorStore()

all_chunks = []

retriever = None


# ==================================================
# LOAD AND INDEX DOCUMENTS
# ==================================================

def initialize_rag():

    global all_chunks
    global retriever

    document_folder = Path(
        "data/legal_documents"
    )

    pdf_files = list(
        document_folder.glob("*.pdf")
    )

    if not pdf_files:

        raise RuntimeError(
            "No PDF files found in "
            "data/legal_documents"
        )

    all_documents = []

    # ----------------------------------------------
    # STEP 1: LOAD PDFs
    # ----------------------------------------------

    for pdf_file in pdf_files:

        print(
            f"Loading: {pdf_file.name}"
        )

        documents = load_pdf(
            pdf_file
        )

        all_documents.extend(
            documents
        )

    print(
        f"Pages loaded: "
        f"{len(all_documents)}"
    )

    # ----------------------------------------------
    # STEP 2: CREATE CHUNKS
    # ----------------------------------------------

    all_chunks = create_chunks(
        all_documents
    )

    print(
        f"Chunks created: "
        f"{len(all_chunks)}"
    )

    # ----------------------------------------------
    # STEP 3: CREATE EMBEDDINGS
    # ----------------------------------------------

    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    embeddings = create_embeddings(
        texts
    )

    print(
        "Embeddings created."
    )

    # ----------------------------------------------
    # STEP 4: CREATE VECTOR DATABASE
    # ----------------------------------------------

    vector_store.create_index(
        embeddings
    )

    print(
        "Vector database created."
    )

    # ----------------------------------------------
    # STEP 5: CREATE RETRIEVER
    # ----------------------------------------------

    retriever = Retriever(
        vector_store,
        all_chunks
    )

    print(
        "RAG system ready!"
    )


# ==================================================
# START APPLICATION
# ==================================================

@app.on_event("startup")
def startup_event():

    initialize_rag()


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/")
def home():

    return {
        "message": "Legal AI Assistant is running."
    }


# ==================================================
# ASK QUESTION
# ==================================================

@app.post(
    "/ask",
    response_model=AnswerResponse
)
def ask_question(
    request: QuestionRequest
):

    global retriever

    if retriever is None:

        raise HTTPException(
            status_code=500,
            detail="RAG system not initialized."
        )

    # ----------------------------------------------
    # STEP 1: RETRIEVE DOCUMENTS
    # ----------------------------------------------

    retrieved_documents = (
        retriever.retrieve(
            request.question,
            top_k=3
        )
    )

    if not retrieved_documents:

        raise HTTPException(
            status_code=404,
            detail="No relevant documents found."
        )

    # ----------------------------------------------
    # STEP 2: GENERATE ANSWER
    # ----------------------------------------------

    answer = generate_answer(
        request.question,
        retrieved_documents
    )

    # ----------------------------------------------
    # STEP 3: CREATE SOURCES
    # ----------------------------------------------

    sources = []

    seen_sources = set()

    for document in retrieved_documents:

        source_key = (
            document["source"],
            document["page"]
        )

        if source_key not in seen_sources:

            sources.append(
                Source(
                    document=document[
                        "source"
                    ],
                    page=document[
                        "page"
                    ]
                )
            )

            seen_sources.add(
                source_key
            )

    # ----------------------------------------------
    # STEP 4: RETURN RESPONSE
    # ----------------------------------------------

    return AnswerResponse(
        answer=answer,
        sources=sources
    )