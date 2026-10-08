DOCUMENT RAG ASSISTANT
=======================

PROJECT OVERVIEW
----------------
Document RAG Assistant is a learning project for understanding and building a Retrieval-Augmented Generation (RAG) system for PDF documents.

The project is being developed step by step so the underlying RAG process is understood before moving to a vector database such as Chroma.

CURRENT RAG PIPELINE
--------------------
PDF
 ↓
Text extraction
 ↓
Chunking
 ↓
Local embeddings
 ↓
NumPy storage
 ↓
Cosine similarity search
 ↓
Top-K relevant chunks
 ↓
Question + retrieved context + instructions
 ↓
OpenAI LLM
 ↓
Answer + page citation + token usage


PROJECT STRUCTURE
-----------------
Document RAG Assistant/
│
├── ingestion.py
│   └── Extracts text from a PDF page by page and preserves page numbers.
│
├── chunker.py
│   └── Splits extracted document text into overlapping chunks while preserving page metadata.
│
├── embedding.py
│   └── Creates embeddings for document chunks using a local Sentence Transformers model.
│
├── embeddings.npy
│   └── NumPy binary file containing saved document embedding vectors.
│
├── similarity_finder.py
│   └── Converts the user's question into an embedding and compares it with saved document embeddings using cosine similarity.
│
├── search.py
│   └── Retrieves relevant chunks, builds the RAG prompt, sends it to the OpenAI model, and returns the answer and token usage.
│
├── app.py
│   └── Streamlit user interface for uploading a PDF, entering a question, displaying the answer, and showing token usage.
│
└── README.md
    └── Project documentation.


INGESTION
---------
ingestion.py uses PyMuPDF (pymupdf).

The PDF is opened from uploaded PDF bytes rather than from a hard-coded filename.

Each extracted page is represented as:

{
    "page_number": 1,
    "text": "..."
}

Only pages containing extracted text are currently returned.

This works for PDFs with a usable text layer. Scanned image-only PDFs would require OCR.


CHUNKING
--------
The document is divided into smaller pieces so the embedding and retrieval system can work with manageable sections of text.

Current settings:

    chunk_size = 800 characters
    overlap = 200 characters

The current approach creates continuous chunks across page boundaries while preserving page numbers.

A chunk can contain text from more than one page:

    {
        "page_numbers": [7, 8],
        "text": "..."
    }

The overlap helps preserve context between neighboring chunks.


EMBEDDINGS
----------
The project uses the local Sentence Transformers model:

    all-MiniLM-L6-v2

The model converts each chunk into a numerical embedding vector.

The model produces 384 values per embedding.

For example:

    40 chunks
        ↓
    40 embedding vectors
        ↓
    NumPy array with shape (40, 384)

Document embeddings are created once and saved rather than recreated for every question.

The user's question is embedded in real time when a search is performed.


EMBEDDINGS STORAGE
------------------
The document embeddings are saved in:

    embeddings.npy

Created with:

    np.save("embeddings.npy", embeddings)

Loaded with:

    embeddings = np.load("embeddings.npy")

The .npy file stores numerical vectors. It does not by itself contain the original chunk text or page metadata.


SIMILARITY SEARCH
-----------------
similarity_finder.py performs manual vector search using NumPy.

Process:

    User question
        ↓
    Question embedding
        ↓
    Compare question vector with all document vectors
        ↓
    Cosine similarity
        ↓
    Rank results
        ↓
    Return Top-K chunks

The current default is:

    TOP_K = 3

This means the three highest-scoring chunks are retrieved.

Cosine similarity measures how closely two vectors point in the same direction. The highest score is treated as the most semantically relevant chunk.


ANSWER GENERATION
-----------------
search.py handles the generation part of RAG.

It receives a question and calls the similarity finder.

The retrieved chunks are combined into a context string.

The prompt contains:

1. Instructions
2. Retrieved document context
3. The user's question

The model is instructed to:

- Answer only using the provided context.
- Not use outside knowledge.
- Say "I don't know." when the answer is not present in the context.
- Cite the page number(s) supporting the answer.
- Not invent page numbers.
- Give a concise answer.

The current answer-generation model is:

    gpt-4o-mini

This is being used because it is sufficient for the current learning task and keeps API costs relatively low.


PAGE CITATIONS
--------------
Each chunk retains page metadata.

For example:

    {
        "pages": [7, 8],
        "text": "..."
    }

The retrieved page information is included in the context given to the LLM.

If a chunk crosses a page boundary, the current system may cite both pages, such as Pages 7-8.

The current citation system is chunk-level rather than sentence-level. It does not yet identify the exact sentence belonging to each page.


STREAMLIT INTERFACE
-------------------
app.py provides the user interface.

Intended user flow:

    Upload PDF
        ↓
    Display uploaded PDF filename
        ↓
    Display number of extracted pages
        ↓
    Show question input
        ↓
    User clicks Ask
        ↓
    search.py processes the question
        ↓
    Display answer
        ↓
    Display token usage

Token usage is displayed as:

    Input Tokens
    Output Tokens
    Total Tokens


TOKEN USAGE
-----------
The OpenAI answer-generation response provides token usage information.

The application displays:

    response.usage.input_tokens
    response.usage.output_tokens
    response.usage.total_tokens

The local Sentence Transformers embedding process does not consume OpenAI API tokens.


IMPORTANT ARCHITECTURE NOTE
---------------------------
The project is currently being transitioned from a fixed-PDF implementation to an uploaded-PDF implementation.

The desired final flow is:

    Streamlit uploaded PDF
        ↓
    ingestion.py
        ↓
    chunker.py
        ↓
    embedding.py
        ↓
    document-specific embeddings + chunk metadata
        ↓
    similarity_finder.py
        ↓
    search.py
        ↓
    Streamlit answer

The uploaded document should generate its own chunks and embeddings. The retrieval system should use those document-specific embeddings rather than embeddings generated from a previously hard-coded PDF.


CURRENT LEARNING OBJECTIVES
---------------------------
The project deliberately implements RAG manually before introducing Chroma.

The manual stage demonstrates:

- PDF ingestion
- Page metadata
- Chunking
- Chunk overlap
- Embeddings
- NumPy arrays
- Cosine similarity
- Top-K retrieval
- Context construction
- Prompt construction
- Grounded answer generation
- Page citations
- Token tracking

After the manual implementation is understood, the next major stage is to replace the manual vector storage/search layer with a vector database such as Chroma.


FUTURE IMPROVEMENTS
-------------------
Planned improvements include:

- Complete arbitrary uploaded-PDF support throughout the entire pipeline.
- Save chunk text and page metadata alongside embeddings.
- Avoid recreating chunks during every search.
- Improve chunk boundaries so sentences are less likely to be cut.
- Tune the optimal Top-K value.
- Improve citation precision.
- Add Chroma as a vector database.
- Add retrieval evaluation.
- Improve handling of scanned PDFs with OCR.
- Improve the Streamlit interface.
- Add support for multiple documents.


PURPOSE OF THE PROJECT
----------------------
The main purpose is educational: to understand how RAG works internally.

The project deliberately starts with:

    Sentence Transformers
    NumPy
    Cosine similarity

before moving to:

    Chroma

This makes it possible to understand what a vector database is actually doing rather than treating it as a black box.
