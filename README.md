# DocuTrust AI

## Enterprise Advanced Retrieval-Augmented Generation (RAG) Platform with Automated Self-Correction

---

## Project Overview

DocuTrust AI is an enterprise-grade Retrieval-Augmented Generation (RAG) platform designed to provide reliable, context-aware, and citation-based answers from uploaded PDF documents. Unlike traditional AI document search systems that often generate hallucinated or unsupported responses, DocuTrust validates retrieved information before generating answers.

The platform implements the Corrective Retrieval-Augmented Generation (CRAG) architecture using LangGraph. It combines semantic search, retrieval validation, query rewriting, and web fallback mechanisms to improve answer accuracy and reliability.

The application enables users to upload enterprise documents, ask natural language questions, and receive trustworthy responses with supporting citations.

---

# Problem Statement

Traditional AI-powered document search systems frequently produce inaccurate or hallucinated responses because they directly generate answers from incomplete or irrelevant retrieved information. These systems lack mechanisms to validate retrieved content before passing it to the language model.

Organizations dealing with policy documents, contracts, compliance manuals, technical documentation, and knowledge bases require a trustworthy document intelligence system capable of generating accurate responses supported by proper citations.

DocuTrust addresses these limitations by implementing an advanced Corrective RAG pipeline that validates retrieved context before generating answers.

---

# Objectives

The main objectives of DocuTrust are:

- Develop an enterprise document question-answering platform.
- Implement semantic document retrieval using vector embeddings.
- Reduce hallucinations through retrieval validation.
- Automatically rewrite ineffective queries.
- Perform fallback web search when document retrieval is insufficient.
- Generate citation-supported responses.
- Store client information and interaction logs.
- Build a responsive and user-friendly web interface.

---

# Key Features

- Upload and process multiple PDF documents
- Semantic document retrieval
- Corrective Retrieval-Augmented Generation (CRAG)
- Cross-Encoder relevance grading
- Automatic query rewriting
- Web search fallback
- Citation-based answer generation
- Real-time agent execution logs
- MongoDB integration
- FastAPI REST backend
- Responsive HTML/CSS/JavaScript frontend

---

# System Architecture

                    User
                      │
                      ▼
            HTML/CSS/JavaScript UI
                      │
                      ▼
                FastAPI Backend
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
    MongoDB                    ChromaDB
(Client Information)      (Vector Database)
        │                           │
        └─────────────┬─────────────┘
                      ▼
            LangGraph CRAG Pipeline
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Retriever      Grading Agent    Query Rewriter
                      │
                      ▼
               Web Search Fallback
                      │
                      ▼
               Response Generator
                      │
                      ▼
           Answer with Source Citations

---

# Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- FastAPI

## Artificial Intelligence

- LangGraph
- LangChain
- Corrective RAG (CRAG)
- Sentence Transformers
- Cross Encoder
- Large Language Models

## Database

- MongoDB
- ChromaDB

## Supporting Libraries

- PyPDF
- Pydantic
- Requests
- Uvicorn

---

# Project Structure

```
ML_MAJOR_PROJECT
│
├── backend
│   ├── app
│   │
│   ├── api
│   ├── ingestion
│   ├── rag
│   │   ├── crag_graph.py
│   │   ├── generator.py
│   │   ├── grader.py
│   │   ├── llm.py
│   │   ├── pipeline.py
│   │   ├── prompts.py
│   │   ├── retriever.py
│   │   ├── store_instance.py
│   │   └── vector_store.py
│   │
│   ├── routers
│   │   ├── ask.py
│   │   ├── clients.py
│   │   ├── documents.py
│   │   └── query.py
│   │
│   ├── services
│   ├── utils
│   │   └── logger.py
│   │
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── chroma_db
├── uploads
├── vector_db
│
├── frontend
│   └── index.html
│
├── requirements.txt
└── README.md
```

---

# Workflow

### Step 1: PDF Upload

Users upload enterprise PDF documents through the web interface.

### Step 2: Text Extraction

The uploaded documents are parsed and text is extracted while preserving the document structure.

### Step 3: Text Chunking

Extracted text is divided into smaller overlapping chunks for efficient semantic retrieval.

### Step 4: Embedding Generation

Each text chunk is converted into vector embeddings using transformer embedding models.

### Step 5: Vector Storage

The embeddings and metadata are stored in ChromaDB.

### Step 6: Semantic Retrieval

Relevant document chunks are retrieved using vector similarity search.

### Step 7: Retrieval Validation

A Cross-Encoder grading model evaluates the relevance of retrieved chunks.

### Step 8: Query Rewriting

If retrieval quality is poor, the user query is automatically rewritten.

### Step 9: Web Search

When document retrieval is insufficient, trusted web sources are searched.

### Step 10: Response Generation

The language model generates an answer using validated context.

### Step 11: Citation Generation

The final response contains citations from uploaded documents and external sources when applicable.

---

# Modules

## PDF Ingestion Module

- Upload PDF documents
- Extract document text
- Parse pages
- Store metadata

## Embedding Module

- Generate vector embeddings
- Convert text into numerical vectors

## Vector Database Module

- Store embeddings
- Retrieve similar vectors
- Manage metadata

## Retriever Module

- Semantic similarity search
- Retrieve relevant document chunks

## Grading Module

- Evaluate retrieval relevance
- Filter irrelevant chunks

## Query Rewriter Module

- Improve poorly formed queries
- Enhance retrieval performance

## Web Search Module

- Retrieve external information when required

## Generator Module

- Generate final validated responses
- Produce citation-supported answers

## MongoDB Module

Stores

- Client Profiles
- Uploaded Documents
- Metadata
- Query History
- Interaction Logs

---

# API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /upload | POST | Upload PDF documents |
| /ask | POST | Submit user questions |
| /clients | GET | Retrieve client information |
| /documents | GET | Retrieve uploaded documents |
| /query | POST | Execute semantic search |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/docutrust.git
```

## Navigate to Project

```bash
cd DocuTrust
```

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file.

```env
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=docutrust
GROQ_API_KEY=your_groq_api_key
CHROMA_DB_PATH=./chroma_db
```

## Start the Backend

```bash
uvicorn app.main:app --reload
```

## Launch the Frontend

Open the `frontend/index.html` file in a browser or use VS Code Live Server.

---

# Advantages

- Reduces hallucinated responses
- Produces citation-backed answers
- Self-correcting retrieval mechanism
- Enterprise-ready architecture
- Fast semantic search
- Scalable and modular design
- Improved document search accuracy
- Transparent response generation

---

# Applications

- Enterprise Knowledge Management
- Corporate Policy Search
- Legal Document Analysis
- Healthcare Documentation
- Banking and Insurance
- Compliance Management
- Research Organizations
- Educational Institutions
- Government Documentation

---

# Future Enhancements

- OCR support for scanned PDFs
- Multilingual document understanding
- Voice-based interaction
- Role-based access control
- Cloud deployment
- Knowledge Graph integration
- Multi-modal Retrieval-Augmented Generation
- Fine-tuned enterprise language models

---

# Conclusion

DocuTrust AI is an enterprise-grade document intelligence platform that combines semantic retrieval, retrieval validation, query rewriting, and web search fallback to generate reliable and citation-supported answers. By implementing the Corrective Retrieval-Augmented Generation (CRAG) architecture, the platform minimizes hallucinations, improves retrieval quality, and delivers trustworthy responses suitable for enterprise environments.

---

