# ⚖️ Legal AI Assistant — RAG-Based Document Question Answering

An AI-powered **Legal Document Question Answering System** built using **Retrieval-Augmented Generation (RAG)**.

The application allows users to ask questions about legal documents such as contracts, agreements, policies, and other PDF documents. Instead of relying only on the LLM's pre-trained knowledge, the system retrieves relevant sections from uploaded documents and uses them as context to generate grounded answers with source references.

---

## 🚀 Features

* 📄 PDF document processing
* 🔍 Automatic text extraction
* ✂️ Text chunking with overlap
* 🧠 Semantic embeddings using Sentence Transformers
* 🗄️ Vector similarity search using FAISS
* 🔎 Top-K relevant document retrieval
* 🤖 LLM-powered answer generation
* 📚 Source and page references
* ⚡ FastAPI backend
* 🔐 Environment-based API key configuration
* 🧩 Modular RAG architecture

---

## 🏗️ System Architecture

```text
                    ⚖️ LEGAL AI ASSISTANT

                         PDF / Documents
                                │
                                ▼
                      Document Extraction
                                │
                                ▼
                            Chunking
                                │
                                ▼
                        Embedding Model
                                │
                                ▼
                         FAISS Vector DB
                                │
                                │
                 ───────────────┼───────────────
                                │
                          User Question
                                │
                                ▼
                        Query Embedding
                                │
                                ▼
                       Similarity Search
                                │
                                ▼
                     Relevant Legal Chunks
                                │
                                ▼
                              LLM
                                │
                         ┌──────┴──────┐
                         ▼             ▼
                      Answer        Sources
```

---

## 🔄 RAG Pipeline

The project consists of two main phases.

### 1. Document Indexing

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Vector Database
```

### 2. Question Answering

```text
User Question
 ↓
Query Embedding
 ↓
Similarity Search
 ↓
Top-K Relevant Chunks
 ↓
LLM
 ↓
Answer + Sources
```

---

## 🧠 How It Works

### Step 1 — Document Extraction

PDF files are loaded using `PyPDF`.

The system extracts text page by page while preserving metadata.

Example:

```python
{
    "text": "Either party may terminate the agreement...",
    "source": "employment_contract.pdf",
    "page": 4
}
```

---

### Step 2 — Chunking

Large documents are divided into smaller chunks.

```text
Large Legal Document
        ↓
┌─────────────────────┐
│ Chunk 1             │
├─────────────────────┤
│ Chunk 2             │
├─────────────────────┤
│ Chunk 3             │
├─────────────────────┤
│ Chunk 4             │
└─────────────────────┘
```

Chunk overlap is used to preserve context between neighboring sections.

---

### Step 3 — Embeddings

Each text chunk is converted into a numerical vector using:

```text
Sentence Transformers
        ↓
all-MiniLM-L6-v2
```

Example:

```text
"30 days written notice"

        ↓

[0.12, -0.45, 0.87, ...]
```

These vectors represent the semantic meaning of the text.

---

### Step 4 — Vector Database

The embeddings are stored in a FAISS index.

```text
Document Chunk
      ↓
Embedding
      ↓
FAISS
```

FAISS allows the application to efficiently search for vectors that are similar to the user's question.

---

### Step 5 — User Question

Example:

> What is the notice period for terminating the contract?

The question is converted into an embedding.

```text
Question
   ↓
Embedding Model
   ↓
Query Vector
```

---

### Step 6 — Similarity Search

The query vector is compared against document vectors.

```text
Query
 ↓
FAISS
 ↓
Top 3 Relevant Chunks
```

For example:

```text
1. Employment Contract — Page 4
2. Employment Contract — Page 5
3. Company Policy — Page 2
```

---

### Step 7 — LLM Generation

The retrieved chunks are provided to the LLM as context.

```text
User Question
      +
Retrieved Legal Context
      ↓
     LLM
      ↓
Grounded Answer
```

The prompt instructs the LLM to use only the supplied document context and avoid inventing information.

---

### Step 8 — Answer + Sources

Example:

```text
Answer:

The contract requires either party to provide
30 days' written notice for termination.

Sources:

📄 employment_contract.pdf
📖 Page 4
```

---

# 📁 Project Structure

```text
legal-ai-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── chunking.py
│   │   └── embeddings.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── generator.py
│   │
│   └── models/
│       ├── __init__.py
│       └── schemas.py
│
├── data/
│   └── legal_documents/
│       └── sample.pdf
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Technologies Used

| Technology            | Purpose                     |
| --------------------- | --------------------------- |
| Python                | Core programming language   |
| FastAPI               | Backend REST API            |
| PyPDF                 | PDF text extraction         |
| Sentence Transformers | Text embeddings             |
| FAISS                 | Vector similarity search    |
| OpenAI API            | LLM-based answer generation |
| Pydantic              | API data validation         |
| NumPy                 | Numerical operations        |
| python-dotenv         | Environment configuration   |

---

# 🔌 API Usage

## Ask a Question

### Endpoint

```text
POST /ask
```

### Request

```json
{
    "question": "What is the notice period for terminating the contract?"
}
```

### Response

```json
{
    "answer": "According to the provided contract, either party must provide 30 days' written notice to terminate the agreement.",
    "sources": [
        {
            "document": "employment_contract.pdf",
            "page": 4
        }
    ]
}
```

---

# 🧪 Example Questions

You can ask questions such as:

```text
What is the termination notice period?

What are the employee's responsibilities?

How many annual leave days are provided?

What happens if the agreement is terminated?

What are the confidentiality requirements?

What are the payment terms?
```

---

# 🧩 Key RAG Components

```text
Document Loader
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embedding Model
      ↓
Vector Store
      ↓
Retriever
      ↓
Context
      ↓
LLM
      ↓
Answer
```

### Component Responsibilities

| Component       | Responsibility                            |
| --------------- | ----------------------------------------- |
| Document Loader | Extract text from PDFs                    |
| Chunking        | Divide documents into manageable sections |
| Embedding Model | Convert text into vectors                 |
| FAISS           | Store and search vectors                  |
| Retriever       | Find relevant chunks                      |
| LLM             | Generate natural-language answers         |
| Metadata        | Track source document and page            |

---

# 🎯 Design Decisions

### Why RAG instead of fine-tuning?

Legal documents can change frequently. RAG allows documents to be updated without retraining the LLM.

### Why embeddings?

Keyword search may fail when the question and document use different words with similar meanings. Embeddings enable semantic search.

### Why FAISS?

FAISS provides efficient vector similarity search and is lightweight enough for a local prototype.

### Why keep page metadata?

Legal answers should be traceable. Page metadata allows the application to show where the retrieved information came from.

---

# ⚠️ Limitations

This project is a **document question-answering system and not a substitute for a qualified lawyer**.

Potential limitations include:

* OCR quality for scanned PDFs
* Incorrect or incomplete document extraction
* Retrieval errors
* Ambiguous legal language
* LLM generation errors
* Lack of jurisdiction-specific legal reasoning

Users should verify important legal information against the original documents and consult a qualified legal professional when appropriate.

---

# 🚀 Future Improvements

The current implementation can be extended with:

```text
Current Version
      ↓
Basic RAG
      ↓
────────────────────────────
      ↓
Hybrid Search
      ↓
Reranking
      ↓
Semantic Chunking
      ↓
Persistent Vector Database
      ↓
Conversation Memory
      ↓
PDF Upload UI
      ↓
Authentication
      ↓
RAG Evaluation
      ↓
Docker
      ↓
Cloud Deployment
```

### Planned Features

* [ ] PDF upload through web interface
* [ ] Multi-document conversations
* [ ] Hybrid keyword + semantic search
* [ ] Cross-encoder reranking
* [ ] Better legal clause extraction
* [ ] Persistent vector database
* [ ] Conversation history
* [ ] Source highlighting
* [ ] RAG evaluation metrics
* [ ] Docker deployment
* [ ] Cloud deployment
* [ ] Automated tests

---

# 📊 Skills Demonstrated

This project demonstrates practical knowledge of:

```text
Python
 │
 ├── Object-Oriented Programming
 ├── File Processing
 ├── APIs
 └── Error Handling

Machine Learning
 │
 ├── Embeddings
 └── Similarity Search

Generative AI
 │
 ├── LLMs
 ├── Prompt Engineering
 └── RAG

Backend
 │
 ├── FastAPI
 ├── REST API
 └── Pydantic

Vector Search
 │
 └── FAISS

Document AI
 │
 ├── PDF Extraction
 ├── Chunking
 └── Metadata
```

---

## ⭐ If you found this project useful

Give the repository a ⭐ and feel free to explore the implementation.

