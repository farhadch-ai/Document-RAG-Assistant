import numpy as np
from sentence_transformers import SentenceTransformer

from ingestion import extract_pages
from chunker import create_chunks


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load document and create chunks




def find_similar_chunks(question,chunks,embeddings, top_k=3):

    # Convert question into an embedding
    question_embedding = model.encode(question)

    # Calculate cosine similarity
    similarities = np.dot(embeddings, question_embedding) / (
        np.linalg.norm(embeddings, axis=1)
        * np.linalg.norm(question_embedding)
    )

    # Get indexes of highest similarity scores
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = []

    for index in top_indices:

        results.append({
            "pages": chunks[index]["page_numbers"],
            "text": chunks[index]["text"],
            "similarity": float(similarities[index])
        })

    return results