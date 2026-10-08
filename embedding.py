from sentence_transformers import SentenceTransformer
import numpy as np




def embed(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)
    embeddings = np.array(embeddings)
    return embeddings






# Get text from every chunk






